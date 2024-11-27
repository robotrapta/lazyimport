from science.pack.slow import Slow
from science.pack.junk import Junk


if __name__ == "__main__":
    slow = Slow()
    junk = Junk()

    print(f"The total number is {slow.number() + junk.number()}")
