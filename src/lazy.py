import sys
import importlib.util
from types import ModuleType

def lazy_load(fullname: str) -> ModuleType:
  try:
    return sys.modules[fullname]
  except KeyError:
    spec = importlib.util.find_spec(fullname)
    module = importlib.util.module_from_spec(spec)
    loader = importlib.util.LazyLoader(spec.loader)
    # Make module with proper locking and get it inserted into sys.modules.
    loader.exec_module(module)
    return module

LAZY_MODULES = [
    "science.pack.slow",
    "science.pack.junk",
]


def setup_lazy_load():
    for module in LAZY_MODULES:
        lazy_load(module)
