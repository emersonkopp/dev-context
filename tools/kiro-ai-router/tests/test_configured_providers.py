"""Tests: router must only choose providers that are properly configured,
skipping unconfigured ones WITHOUT spending quota or raising (TDD Red).
"""
import pytest

from kiro_ai_router import core


def _cfg(tmp_path, monkeypatch, text):
    p = tmp_path / 'config.yaml'
    p.write_text(text)
    monkeypatch.setenv('KIRO_AI_ROUTER_CONFIG', str(p))
    return p


# ---------------------------------------------------------------------------
# is_configured(provider): pure check, no network, based on env/config.
# ---------------------------------------------------------------------------
def test_ollama_always_candidate():
    # Ollama is the local base provider; treated as configured.
    assert core.is_configured('ollama', core.config()) is True


def test_groq_configured_requires_key(monkeypatch):
    monkeypatch.delenv('GROQ_API_KEY', raising=False)
    assert core.is_configured('groq', core.config()) is False
    monkeypatch.setenv('GROQ_API_KEY', 'gsk-x')
    assert core.is_configured('groq', core.config()) is True


def test_openrouter_requires_key_and_free_model(monkeypatch):
    monkeypatch.delenv('OPENROUTER_API_KEY', raising=False)
    monkeypatch.delenv('OPENROUTER_FREE_MODEL', raising=False)
    assert core.is_configured('openrouter', core.config()) is False
    monkeypatch.setenv('OPENROUTER_API_KEY', 'k')
    # key but model not ":free" -> still not configured
    monkeypatch.setenv('OPENROUTER_FREE_MODEL', 'some/model')
    assert core.is_configured('openrouter', core.config()) is False
    monkeypatch.setenv('OPENROUTER_FREE_MODEL', 'some/model:free')
    assert core.is_configured('openrouter', core.config()) is True


def test_gemini_requires_key(monkeypatch):
    monkeypatch.delenv('GEMINI_API_KEY', raising=False)
    monkeypatch.delenv('GOOGLE_API_KEY', raising=False)
    assert core.is_configured('gemini', core.config()) is False
    monkeypatch.setenv('GOOGLE_API_KEY', 'g')
    assert core.is_configured('gemini', core.config()) is True


# ---------------------------------------------------------------------------
# delegate() must skip unconfigured providers BEFORE reserving quota.
# ---------------------------------------------------------------------------
def test_delegate_skips_unconfigured_cloud_without_spending_quota(monkeypatch, tmp_path):
    _cfg(tmp_path, monkeypatch, 'cloud_enabled: true\nroutes:\n  general: [ollama, groq, openrouter, gemini]\n')
    monkeypatch.setattr(core, 'DATA', tmp_path)
    # Local fails; cloud providers are NOT configured (no keys) -> must be skipped.
    monkeypatch.setattr(core, 'ollama', lambda *a, **k: (_ for _ in ()).throw(RuntimeError('down')))
    # If any unconfigured provider were reserved/called it would be a bug:
    monkeypatch.setattr(core, 'groq', lambda *a, **k: (_ for _ in ()).throw(AssertionError('groq should be skipped')))
    monkeypatch.setattr(core, 'openrouter', lambda *a, **k: (_ for _ in ()).throw(AssertionError('openrouter should be skipped')))
    monkeypatch.setattr(core, 'gemini', lambda *a, **k: (_ for _ in ()).throw(AssertionError('gemini should be skipped')))

    result = core.delegate('do it', 'general', local_only=False)
    assert result['status'] == 'unavailable'
    # Only ollama should have been attempted; cloud skipped (not "limit reached", not called).
    # Quota must not be spent on unconfigured providers.
    usage = core.usage()
    spent = {c['provider'] for c in usage['counts']}
    assert 'groq' not in spent
    assert 'openrouter' not in spent
    assert 'gemini' not in spent


def test_delegate_uses_only_configured_cloud(monkeypatch, tmp_path):
    _cfg(tmp_path, monkeypatch, 'cloud_enabled: true\nroutes:\n  general: [ollama, groq, openrouter, gemini]\n')
    monkeypatch.setattr(core, 'DATA', tmp_path)
    monkeypatch.setattr(core, 'ollama', lambda *a, **k: (_ for _ in ()).throw(RuntimeError('down')))
    # Only groq configured
    monkeypatch.setenv('GROQ_API_KEY', 'gsk-x')
    monkeypatch.setattr(core, 'groq', lambda prompt: ('from-groq', 'groq-model'))
    monkeypatch.setattr(core, 'openrouter', lambda *a, **k: (_ for _ in ()).throw(AssertionError('openrouter not configured')))
    monkeypatch.setattr(core, 'gemini', lambda *a, **k: (_ for _ in ()).throw(AssertionError('gemini not configured')))

    result = core.delegate('do it', 'general', local_only=False)
    assert result['status'] == 'success'
    assert result['provider'] == 'groq'
