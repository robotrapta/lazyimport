import sys
import importlib.util
from types import ModuleType

class LazyObject:
    def __init__(self, module_name, attr_name):
        self._module_name = module_name
        self._attr_name = attr_name
        self._real_object = None

    def _load(self):
        if self._real_object is None:
            module = sys.modules[self._module_name]
            module.__loader__.exec_module(module)
            self._real_object = getattr(module, self._attr_name)

    def __call__(self, *args, **kwargs):
        self._load()
        return self._real_object(*args, **kwargs)

    def __getattr__(self, name):
        self._load()
        return getattr(self._real_object, name)

def lazy_load(fullname: str) -> ModuleType:
    try:
        return sys.modules[fullname]
    except KeyError:
        spec = importlib.util.find_spec(fullname)
        module = importlib.util.module_from_spec(spec)
        loader = importlib.util.LazyLoader(spec.loader)
        module.__loader__ = loader
        sys.modules[fullname] = module
        
        # Add __getattr__ to handle "from ... import ..." statements
        def __getattr__(name):
            # Return a LazyObject instead of loading the module
            return LazyObject(fullname, name)
        
        module.__getattr__ = __getattr__
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
