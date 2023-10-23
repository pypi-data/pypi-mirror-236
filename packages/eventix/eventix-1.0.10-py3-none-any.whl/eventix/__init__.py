import importlib

import toml
from pathlib import Path


def get_version():
    try:
        path = Path(__file__).resolve().parents[1] / 'pyproject.toml'
        pyproject = toml.loads(open(str(path)).read())
        v = pyproject['tool']['poetry']['version']

    except Exception:
        try:
            v = importlib.metadata.version('eventix')
        except Exception:
            v = "0.0.0"
    return v


__version__ = get_version()
