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
            # Now actually load the module by calling the loader
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


def _get_lazy_object(fullname, name) -> LazyObject:
    """
    Get an attribute from the module, returning a LazyObject if necessary.

    Args:
        fullname (str): The full name of the module.
        name (str): The name of the attribute.

    Returns:
        LazyObject: A proxy object for the attribute.
    """
    return LazyObject(fullname, name)


def setup_lazyload_module(fullname: str):
    """
    Create an entry in sys.modules for a module that we don't want to load until
    it is accessed.

    Args:
        fullname (str): The full name of the module to be lazily loaded.

    Example:
        setup_lazyload_module("science.pack.slow")

    After calling setup_lazyload_module("science.pack.slow") you can do:
        import science.pack.slow  # won't actually load the module
    And even:
        from science.pack.slow import Something
    Which _still_ doesn't load the module.  But as soon as you call `Something()`
    then it will load the module and return the result.
    """
    try:
        _ = sys.modules[fullname]
        return
    except KeyError:
        # It's not already loaded, so we need to set up the proxy module.
        pass

    spec = importlib.util.find_spec(fullname)
    module = importlib.util.module_from_spec(spec)
    loader = importlib.util.LazyLoader(spec.loader)
    module.__loader__ = loader
    sys.modules[fullname] = module
    
    # Add __getattr__ to handle "from ... import ..." statements
    module.__getattr__ = lambda name: _get_lazy_object(fullname, name)
    sys.modules[fullname] = module
