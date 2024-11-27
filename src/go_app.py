from lazy import setup_lazy_load
setup_lazy_load()

from app.mylib import MyLib

if __name__ == "__main__":
    mylib = MyLib()
    mylib.hello()
