import sys
import importlib.util
from types import ModuleType

class LazyObject:
    """A proxy object that delays the loading of a module attribute until it is accessed.
    When you call `from foo import bar` the `bar` is a LazyObject which allows the 
    code to run without actually importing the foo module.
    But once you call `bar.baz` the `bar` object will load the `foo` module and return.
    """

    def __init__(self, module_name, attr_name):
        """
        Args:
            module_name (str): The name of the module.
            attr_name (str): The name of the attribute to be lazily loaded.
        """
        self._module_name = module_name
        self._attr_name = attr_name
        self._real_object = None

    def _load(self):
        """Load the real object from the module if it hasn't been loaded yet."""
        if self._real_object is None:
            module = sys.modules[self._module_name]
            module.__loader__.exec_module(module)
            self._real_object = getattr(module, self._attr_name)

    def __call__(self, *args, **kwargs):
        """
        Call the real object, loading it if necessary.

        Args:
            *args: Positional arguments for the call.
            **kwargs: Keyword arguments for the call.

        Returns:
            The result of calling the real object.
        """
        self._load()
        return self._real_object(*args, **kwargs)

    def __getattr__(self, name):
        """
        Get an attribute of the real object, loading it if necessary.

        Args:
            name (str): The name of the attribute.

        Returns:
            The attribute of the real object.
        """
        self._load()
        return getattr(self._real_object, name)

def lazy_load(fullname: str) -> ModuleType:
    """
    Lazily load a module, returning a proxy module that delays loading until accessed.

    Args:
        fullname (str): The full name of the module to be lazily loaded.

    Returns:
        ModuleType: A proxy module that delays loading.
    """
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
            """
            Get an attribute from the module, returning a LazyObject if necessary.

            Args:
                name (str): The name of the attribute.

            Returns:
                LazyObject: A proxy object for the attribute.
            """
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
