from science.pack.slow import Slow
from science.pack.junk import Junk

class SciApp():
    def __init__(self):
        self.slow = Slow()
        self.junk = Junk()

    def hello(self):
        print("Science app says Hi")

    def number(self) -> int:
        return self.slow.number() + self.junk.number()

class MyLib:
    def __init__(self):
        pass

    def hello(self):
        print("MyLib is here")

    def do_science(self):
        science = SciApp()
        print(f"The total number is {science.number()}")