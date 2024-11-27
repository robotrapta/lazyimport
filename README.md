This is a fake project to test out fast/lazy loading of python modules.
It simulates an app which has import dependences on science packages.
The science packages are slow to load, so we want to lazy load them.

The project confirms that the app can run with code references to the science packages,
but the science packages are not loaded until they are first used.
