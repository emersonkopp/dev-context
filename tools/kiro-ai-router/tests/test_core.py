from kiro_ai_router import core


def _isolate(monkeypatch, tmp_path, yaml_text=''):
    """Point config at an isolated file so tests never read the user's real config."""
    monkeypatch.setattr(core, 'DATA', tmp_path)
    cfg = tmp_path / 'config.yaml'
    cfg.write_text(yaml_text)
    monkeypatch.setenv('KIRO_AI_ROUTER_CONFIG', str(cfg))


def test_default_local_only(monkeypatch, tmp_path):
    _isolate(monkeypatch, tmp_path)
    monkeypatch.setattr(core, 'ollama', lambda prompt, task_type, cfg: ('ok', 'local'))
    result = core.delegate('Summarize a function', 'docs')
    assert result['status'] == 'success'
    assert result['provider'] == 'ollama'


def test_secret_rejection(monkeypatch, tmp_path):
    _isolate(monkeypatch, tmp_path)
    result = core.delegate('Review sk-abcdefghijklmnopqrstuv', 'review')
    assert result['status'] == 'rejected'


def test_invalid_type(monkeypatch, tmp_path):
    _isolate(monkeypatch, tmp_path)
    assert core.delegate('Hello', 'unknown')['status'] == 'rejected'


def test_cloud_disabled_blocks_cloud_even_when_not_local_only(monkeypatch, tmp_path):
    # cloud_enabled defaults to false -> no cloud provider may run, so when the
    # local provider fails the result must be 'unavailable', never a cloud call.
    _isolate(monkeypatch, tmp_path, 'cloud_enabled: false\n')
    monkeypatch.setattr(core, 'ollama', lambda *a, **k: (_ for _ in ()).throw(RuntimeError('offline')))
    monkeypatch.setattr(core, 'groq', lambda prompt: ('cloud', 'groq'))
    monkeypatch.setattr(core, 'openrouter', lambda prompt: ('cloud', 'or'))
    result = core.delegate('Explain this', 'code', local_only=False)
    assert result['status'] == 'unavailable'


def test_cloud_requires_local_only_false(monkeypatch, tmp_path):
    # Even with cloud_enabled true, local_only=True must keep everything local.
    _isolate(monkeypatch, tmp_path, 'cloud_enabled: true\n')
    monkeypatch.setattr(core, 'ollama', lambda *a, **k: (_ for _ in ()).throw(RuntimeError('offline')))
    monkeypatch.setattr(core, 'groq', lambda prompt: ('cloud', 'groq'))
    result = core.delegate('Explain this', 'code', local_only=True)
    assert result['status'] == 'unavailable'
