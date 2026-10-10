from pathlib import Path
import importlib.util
import os
import sys

LOCAL_DEPS = Path(__file__).with_name(".deps")
PYGAME_BINARY = f"base.cp{sys.version_info.major}{sys.version_info.minor}-win_amd64.pyd"
LOCAL_PYGAME_MATCHES = (LOCAL_DEPS / "pygame" / PYGAME_BINARY).exists()

if LOCAL_PYGAME_MATCHES:
    sys.path.insert(0, str(LOCAL_DEPS))
elif importlib.util.find_spec("pygame") is None:
    bundled_python = Path.home() / ".cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe"
    if bundled_python.exists() and Path(sys.executable).resolve() != bundled_python.resolve():
        os.execv(str(bundled_python), [str(bundled_python), str(Path(__file__).resolve()), *sys.argv[1:]])
    expected = f"Pygame compatible avec Python {sys.version_info.major}.{sys.version_info.minor}"
    raise SystemExit(
        f"{expected} introuvable. Lancez lancer_kitten_front.bat ou installez pygame avec :\n"
        f'"{sys.executable}" -m pip install pygame'
    )

from pygame_app import run

if __name__ == "__main__":
    run()
