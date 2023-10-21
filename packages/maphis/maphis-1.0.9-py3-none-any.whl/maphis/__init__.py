import importlib.resources

__version__ = '1.0.9'

from pathlib import Path

# with importlib.resources.path('maphis', '__main__.py') as p:
#     MAPHIS_PATH = p.parent

MAPHIS_PATH = Path(__file__).parent

print(f"MAPHIS_PATH is {MAPHIS_PATH}")

MAPHIS_VERSION = __version__