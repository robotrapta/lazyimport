from lazy import setup_lazy_load
setup_lazy_load()

from app.mylib import MyLib

setup_lazy_load()

if __name__ == "__main__":
    mylib = MyLib()
    mylib.hello()
