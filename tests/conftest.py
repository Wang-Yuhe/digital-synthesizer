import sys
import types
import pytest

@pytest.fixture(autouse=True, scope="session")
def mock_sounddevice():
    """在整个测试会话中 mock 掉 sounddevice"""
    mock_sd = types.SimpleNamespace(
        play=lambda *args, **kwargs: None,
        wait=lambda: None
    )
    sys.modules["sounddevice"] = mock_sd
