"""Shared test fixtures.

Isolation guardrail: by default no test should read the user's real
~/.config/kiro-ai-router/config.yaml nor pick up real cloud credentials from
the environment. This prevents flaky tests and, critically, accidental real
network calls / cost during the suite. Tests that need specific config set
KIRO_AI_ROUTER_CONFIG themselves (the autouse fixture only provides a default).
"""
import pytest


@pytest.fixture(autouse=True)
def isolate_router_env(monkeypatch, tmp_path):
    # Default to an empty, isolated config unless a test overrides it.
    default_cfg = tmp_path / '_default_config.yaml'
    default_cfg.write_text('')
    monkeypatch.setenv('KIRO_AI_ROUTER_CONFIG', str(default_cfg))
    # Strip real cloud credentials so no test can hit a live provider.
    for var in ('OPENROUTER_API_KEY', 'OPENROUTER_FREE_MODEL', 'GROQ_API_KEY',
                'GROQ_MODEL', 'GROQ_ALLOWED_MODELS', 'GEMINI_API_KEY', 'GOOGLE_API_KEY',
                'GEMINI_MODEL', 'GEMINI_ALLOWED_MODELS'):
        monkeypatch.delenv(var, raising=False)
    yield
