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
    "science",
    "science.pack",
    "science.pack.slow",
    "science.pack.junk",
]


def show_modules():
    print("sys.modules:")
    for m in [
        "science",
        "science.pack",
        "science.pack.slow",
        "science.pack.junk",
    ]:
        try:
            print(f"  {m}: {sys.modules[m]}")
        except KeyError:
            print(f"  {m}: <not loaded>")
    print("End of sys.modules")


def setup_lazy_load():
    print(f"sys.modules before lazy loading:")
    show_modules()
    print("Setting up lazy loading for modules:")
    for module in LAZY_MODULES:
        print(f"  {module}")
        sys.modules[module] = lazy_load(module)

    print("\n\nModules after lazy loading:")
    show_modules()
