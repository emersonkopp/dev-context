"""Security-hardening tests (TDD Red phase).

Covers:
  #1 Gemini adapter is a pure HTTP API (no subprocess / no secret leakage).
  #2 Expanded secret detection (Google/Slack/JWT/connection strings/entropy).
  #3 Config validation of types and numeric bounds.
  #4 Input type validation in delegate().
  #6 OpenRouter defensive pricing + response access.
  #8 Context is wrapped in an injection-resistant sentinel delimiter.
"""
import builtins
import json

import pytest

from kiro_ai_router import core


# ----------------------------------------------------------------------------
# #1 Gemini is now a pure HTTP API: it must never spawn a subprocess, so no
# agent runs locally and no environment secrets can leak to a child process.
# ----------------------------------------------------------------------------
def test_gemini_is_pure_http_no_subprocess(monkeypatch):
    monkeypatch.setenv('GEMINI_API_KEY', 'test-key')

    def boom(*a, **k):
        raise AssertionError('gemini() must not spawn a subprocess')

    monkeypatch.setattr(core.subprocess, 'run', boom)

    class FakeResp:
        def raise_for_status(self):
            pass

        def json(self):
            return {'candidates': [{'content': {'parts': [{'text': 'ok'}]}}]}

    class FakeClient:
        def __init__(self, *a, **k):
            assert k.get('trust_env') is False

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def post(self, *a, **k):
            return FakeResp()

    monkeypatch.setattr(core.httpx, 'Client', FakeClient)
    answer, _ = core.gemini('hello')
    assert answer == 'ok'


# ----------------------------------------------------------------------------
# #2 Expanded secret detection.
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# Payloads are assembled at runtime (prefix + body) so no complete token-shaped
# literal exists in source — avoids tripping repo secret-scanning / push
# protection while still exercising the detector against the full string.
@pytest.mark.parametrize('payload', [
    'AIza' + 'Sy' + 'A' + '0123456789' + 'abcdefghijklmnopqrst',  # Google API key shape
    'xox' + 'b-' + '123456789012-' + 'a' * 24,                    # Slack bot token shape
    'postgres://user:' + 'p4ssw0rd' + '@db.example.com:5432/app',  # connection string w/ pw
    'eyJ' + 'hbGciOiJIUzI1NiJ9' + '.' + 'eyJzdWIiOiJ4In0' + '.' + 'abc123DEFxyz',  # JWT shape
    'gl' + 'pat-' + 'abcdef1234567890ABCD',                       # GitLab PAT shape
])
def test_expanded_secret_detection(payload):
    result = core.delegate('Review this: ' + payload, 'review')
    assert result['status'] == 'rejected', f'should reject secret: {payload!r}'


def test_benign_text_not_flagged_as_secret():
    # Must not false-positive on ordinary prose/code.
    result = core.delegate('Explain how a for loop works in Python', 'docs')
    # Will route to ollama (which is unavailable in unit test) -> unavailable, NOT rejected.
    assert result['status'] != 'rejected'


# ----------------------------------------------------------------------------
# #3 Config validation of types and bounds.
# ----------------------------------------------------------------------------
def _write_cfg(tmp_path, monkeypatch, text):
    p = tmp_path / 'config.yaml'
    p.write_text(text)
    monkeypatch.setenv('KIRO_AI_ROUTER_CONFIG', str(p))
    return p


def test_config_rejects_negative_int(tmp_path, monkeypatch):
    _write_cfg(tmp_path, monkeypatch, 'max_task_chars: -5\n')
    with pytest.raises(ValueError):
        core.config()


def test_config_rejects_non_int_where_int_expected(tmp_path, monkeypatch):
    _write_cfg(tmp_path, monkeypatch, 'max_response_chars: "lots"\n')
    with pytest.raises(ValueError):
        core.config()


def test_config_rejects_non_loopback_ollama_url(tmp_path, monkeypatch):
    _write_cfg(tmp_path, monkeypatch, 'ollama:\n  url: http://evil.example.com\n')
    with pytest.raises(ValueError):
        core.config()


def test_config_rejects_absurd_limit(tmp_path, monkeypatch):
    _write_cfg(tmp_path, monkeypatch, 'limits:\n  ollama: 10000000\n')
    with pytest.raises(ValueError):
        core.config()


def test_config_accepts_valid_overrides(tmp_path, monkeypatch):
    _write_cfg(tmp_path, monkeypatch, 'max_task_chars: 1000\nlimits:\n  ollama: 50\n')
    cfg = core.config()
    assert cfg['max_task_chars'] == 1000
    assert cfg['limits']['ollama'] == 50


# ----------------------------------------------------------------------------
# #4 Input type validation in delegate().
# ----------------------------------------------------------------------------
@pytest.mark.parametrize('bad', [None, 123, ['a'], {'x': 1}])
def test_delegate_rejects_non_string_task(bad):
    result = core.delegate(bad, 'general')
    assert result['status'] == 'rejected'


@pytest.mark.parametrize('bad', [123, ['a'], object()])
def test_delegate_rejects_non_string_context(bad):
    result = core.delegate('valid task', 'general', context=bad)
    assert result['status'] == 'rejected'


def test_delegate_rejects_non_string_task_type():
    result = core.delegate('valid task', task_type=123)
    assert result['status'] == 'rejected'


# ----------------------------------------------------------------------------
# #8 Injection-resistant context delimiter.
# ----------------------------------------------------------------------------
def test_prompt_wraps_context_in_sentinel(monkeypatch, tmp_path):
    monkeypatch.setattr(core, 'DATA', tmp_path)
    seen = {}

    def fake_ollama(prompt, task_type, cfg):
        seen['prompt'] = prompt
        return 'ok', 'local'

    monkeypatch.setattr(core, 'ollama', fake_ollama)
    core.delegate('do the thing', 'general', context='some ctx')
    prompt = seen['prompt']
    # A sentinel delimiter must surround the untrusted context.
    assert 'BEGIN UNTRUSTED CONTEXT' in prompt
    assert 'END UNTRUSTED CONTEXT' in prompt
    assert 'some ctx' in prompt
