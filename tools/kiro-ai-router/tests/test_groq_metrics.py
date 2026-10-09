"""Tests for the Groq adapter and local observability metrics (TDD Red).

Cost constraint: metrics MUST be computed only from the local SQLite data the
router already persists. No network calls, no paid services, no tokenizer.
"""
import json

import pytest

from kiro_ai_router import core


# ---------------------------------------------------------------------------
# Groq adapter: same safe shape as openrouter() but a pure HTTP API.
# ---------------------------------------------------------------------------
def test_groq_missing_key_raises(monkeypatch):
    monkeypatch.delenv('GROQ_API_KEY', raising=False)
    with pytest.raises(RuntimeError):
        core.groq('hello')


def test_groq_success(monkeypatch):
    monkeypatch.setenv('GROQ_API_KEY', 'gsk-test-key')
    monkeypatch.setenv('GROQ_MODEL', 'llama-3.1-8b-instant')

    class FakeResp:
        def raise_for_status(self):
            pass

        def json(self):
            return {'choices': [{'message': {'content': 'GROQ_OK'}}]}

    class FakeClient:
        def __init__(self, *a, **k):
            # trust_env must be disabled, like the other adapters.
            assert k.get('trust_env') is False

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def post(self, url, headers=None, json=None, timeout=None):
            assert url.startswith('https://api.groq.com/')
            assert headers['Authorization'].startswith('Bearer ')
            assert json['max_tokens'] <= 768
            return FakeResp()

    monkeypatch.setattr(core.httpx, 'Client', FakeClient)
    answer, model = core.groq('hello')
    assert answer == 'GROQ_OK'
    assert model == 'llama-3.1-8b-instant'


def test_groq_malformed_response(monkeypatch):
    monkeypatch.setenv('GROQ_API_KEY', 'gsk-test-key')
    monkeypatch.setenv('GROQ_MODEL', 'llama-3.1-8b-instant')

    class FakeResp:
        def raise_for_status(self):
            pass

        def json(self):
            return {'unexpected': True}

    class FakeClient:
        def __init__(self, *a, **k):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def post(self, *a, **k):
            return FakeResp()

    monkeypatch.setattr(core.httpx, 'Client', FakeClient)
    with pytest.raises(ValueError):
        core.groq('hello')


def test_groq_in_defaults_routes_and_limits():
    assert 'groq' in core.DEFAULTS['limits']
    for route in core.DEFAULTS['routes'].values():
        assert isinstance(route, list)
    # groq must appear in at least the general route
    assert 'groq' in core.DEFAULTS['routes']['general']


def test_groq_allowlist_blocks_unlisted_model(monkeypatch):
    monkeypatch.setenv('GROQ_API_KEY', 'gsk-test')
    monkeypatch.setenv('GROQ_MODEL', 'some/expensive-model')
    monkeypatch.setenv('GROQ_ALLOWED_MODELS', 'openai/gpt-oss-20b,openai/gpt-oss-120b')

    # Must fail BEFORE any network call.
    def boom(*a, **k):
        raise AssertionError('must not reach network when model is not allowlisted')

    monkeypatch.setattr(core.httpx, 'Client', boom)
    with pytest.raises(RuntimeError):
        core.groq('hello')


def test_groq_allowlist_allows_listed_model(monkeypatch):
    monkeypatch.setenv('GROQ_API_KEY', 'gsk-test')
    monkeypatch.setenv('GROQ_MODEL', 'openai/gpt-oss-20b')
    monkeypatch.setenv('GROQ_ALLOWED_MODELS', 'openai/gpt-oss-20b,openai/gpt-oss-120b')

    class FakeResp:
        def raise_for_status(self):
            pass

        def json(self):
            return {'choices': [{'message': {'content': 'ALLOWED_OK'}}]}

    class FakeClient:
        def __init__(self, *a, **k):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def post(self, *a, **k):
            return FakeResp()

    monkeypatch.setattr(core.httpx, 'Client', FakeClient)
    answer, model = core.groq('hello')
    assert answer == 'ALLOWED_OK'
    assert model == 'openai/gpt-oss-20b'


def test_groq_no_allowlist_is_backward_compatible(monkeypatch):
    # When GROQ_ALLOWED_MODELS is unset, any model is permitted (no breakage).
    monkeypatch.setenv('GROQ_API_KEY', 'gsk-test')
    monkeypatch.setenv('GROQ_MODEL', 'anything/at-all')
    monkeypatch.delenv('GROQ_ALLOWED_MODELS', raising=False)

    class FakeResp:
        def raise_for_status(self):
            pass

        def json(self):
            return {'choices': [{'message': {'content': 'OK'}}]}

    class FakeClient:
        def __init__(self, *a, **k):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def post(self, *a, **k):
            return FakeResp()

    monkeypatch.setattr(core.httpx, 'Client', FakeClient)
    answer, _ = core.groq('hello')
    assert answer == 'OK'


def test_groq_delegates_as_cloud(monkeypatch, tmp_path):
    monkeypatch.setattr(core, 'DATA', tmp_path)
    # local fails -> should try groq when cloud enabled + not local_only
    monkeypatch.setattr(core, 'ollama', lambda *a, **k: (_ for _ in ()).throw(RuntimeError('down')))
    monkeypatch.setenv('GROQ_API_KEY', 'gsk-test')  # groq must be configured to be chosen
    monkeypatch.setattr(core, 'groq', lambda prompt: ('from-groq', 'llama'))
    monkeypatch.setenv('KIRO_AI_ROUTER_CONFIG', str(_cfg(tmp_path, 'cloud_enabled: true\nroutes:\n  general: [ollama, groq]\n')))
    result = core.delegate('do it', 'general', local_only=False)
    assert result['status'] == 'success'
    assert result['provider'] == 'groq'


def _cfg(tmp_path, text):
    p = tmp_path / 'config.yaml'
    p.write_text(text)
    return p


# ---------------------------------------------------------------------------
# Local observability metrics: insights() computed from SQLite only.
# ---------------------------------------------------------------------------
def test_insights_empty(monkeypatch, tmp_path):
    monkeypatch.setattr(core, 'DATA', tmp_path)
    data = core.insights()
    assert data['totals']['calls'] == 0
    assert data['totals']['success'] == 0
    assert data['estimated_tokens_offloaded'] == 0
    assert 'by_provider' in data


def test_insights_counts_and_success_rate(monkeypatch, tmp_path):
    monkeypatch.setattr(core, 'DATA', tmp_path)
    monkeypatch.setattr(core, 'ollama', lambda prompt, task_type, cfg: ('a local answer', 'local'))
    # 3 successful local delegations
    for _ in range(3):
        assert core.delegate('explain loops', 'docs')['status'] == 'success'
    data = core.insights()
    assert data['totals']['calls'] == 3
    assert data['totals']['success'] == 3
    assert data['totals']['success_rate'] == 1.0
    # tokens offloaded estimated from stored prompt/response char counts (>0)
    assert data['estimated_tokens_offloaded'] > 0
    assert data['by_provider']['ollama']['success'] == 3


def test_insights_tracks_errors_separately(monkeypatch, tmp_path):
    monkeypatch.setattr(core, 'DATA', tmp_path)
    monkeypatch.setattr(core, 'ollama', lambda *a, **k: (_ for _ in ()).throw(RuntimeError('boom')))
    core.delegate('explain loops', 'docs')  # fails, local only
    data = core.insights()
    assert data['totals']['errors'] >= 1
    assert data['totals']['success_rate'] < 1.0


def test_insights_no_network(monkeypatch, tmp_path):
    """insights() must never open an httpx client (cost guardrail)."""
    monkeypatch.setattr(core, 'DATA', tmp_path)

    def boom(*a, **k):
        raise AssertionError('insights must not make network calls')

    monkeypatch.setattr(core.httpx, 'Client', boom)
    core.insights()  # must not raise
