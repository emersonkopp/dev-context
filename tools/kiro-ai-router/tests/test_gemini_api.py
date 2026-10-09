"""Tests for the Gemini HTTP API adapter (TDD Red).

The adapter MUST be a pure HTTP call (no subprocess / CLI) and enforce a model
allowlist as a cost safeguard, failing closed before any network call.
"""
import pytest

from kiro_ai_router import core


def test_gemini_missing_key_raises(monkeypatch):
    monkeypatch.delenv('GEMINI_API_KEY', raising=False)
    monkeypatch.delenv('GOOGLE_API_KEY', raising=False)
    with pytest.raises(RuntimeError):
        core.gemini('hello')


def test_gemini_uses_cheap_default_model(monkeypatch):
    monkeypatch.setenv('GEMINI_API_KEY', 'test-key')
    monkeypatch.delenv('GEMINI_MODEL', raising=False)
    captured = {}

    class FakeResp:
        def raise_for_status(self):
            pass

        def json(self):
            return {'candidates': [{'content': {'parts': [{'text': 'GEMINI_OK'}]}}]}

    class FakeClient:
        def __init__(self, *a, **k):
            assert k.get('trust_env') is False

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def post(self, url, headers=None, json=None, timeout=None, params=None):
            captured['url'] = url
            captured['json'] = json
            return FakeResp()

    monkeypatch.setattr(core.httpx, 'Client', FakeClient)
    answer, model = core.gemini('hello')
    assert answer == 'GEMINI_OK'
    # Default must be the cheapest flash model.
    assert model == 'gemini-flash-lite-latest'
    assert 'gemini-flash-lite-latest' in captured['url']
    # No subprocess should ever be used.


def test_gemini_is_pure_http_no_subprocess(monkeypatch):
    monkeypatch.setenv('GEMINI_API_KEY', 'test-key')

    def boom(*a, **k):
        raise AssertionError('gemini() must not spawn a subprocess')

    monkeypatch.setattr(core.subprocess, 'run', boom)

    class FakeResp:
        def raise_for_status(self):
            pass

        def json(self):
            return {'candidates': [{'content': {'parts': [{'text': 'OK'}]}}]}

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
    answer, _ = core.gemini('hello')
    assert answer == 'OK'


def test_gemini_allowlist_blocks_unlisted_model(monkeypatch):
    monkeypatch.setenv('GEMINI_API_KEY', 'test-key')
    monkeypatch.setenv('GEMINI_MODEL', 'gemini-1.5-pro')  # expensive, not allowed
    monkeypatch.setenv('GEMINI_ALLOWED_MODELS', 'gemini-1.5-flash-8b,gemini-1.5-flash')

    def boom(*a, **k):
        raise AssertionError('must not reach network when model is not allowlisted')

    monkeypatch.setattr(core.httpx, 'Client', boom)
    with pytest.raises(RuntimeError):
        core.gemini('hello')


def test_gemini_allowlist_allows_listed_model(monkeypatch):
    monkeypatch.setenv('GEMINI_API_KEY', 'test-key')
    monkeypatch.setenv('GEMINI_MODEL', 'gemini-1.5-flash')
    monkeypatch.setenv('GEMINI_ALLOWED_MODELS', 'gemini-1.5-flash-8b,gemini-1.5-flash')

    class FakeResp:
        def raise_for_status(self):
            pass

        def json(self):
            return {'candidates': [{'content': {'parts': [{'text': 'ALLOWED'}]}}]}

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
    answer, model = core.gemini('hello')
    assert answer == 'ALLOWED'
    assert model == 'gemini-1.5-flash'


def test_gemini_malformed_response(monkeypatch):
    monkeypatch.setenv('GEMINI_API_KEY', 'test-key')

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
        core.gemini('hello')


def test_gemini_blocked_by_safety_raises(monkeypatch):
    # No candidates (e.g. blocked by safety) must raise, not return empty.
    monkeypatch.setenv('GEMINI_API_KEY', 'test-key')

    class FakeResp:
        def raise_for_status(self):
            pass

        def json(self):
            return {'candidates': []}

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
        core.gemini('hello')
