import sys
import importlib.util
from types import ModuleType

from lazyloadtools import setup_lazyload_module


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
        setup_lazyload_module(module)

    print("\n\nModules after lazy loading:")
    show_modules()
