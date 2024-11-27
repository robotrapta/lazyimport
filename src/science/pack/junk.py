import time

from tqdm.auto import tqdm

class Junk():
    def __init__(self):
        pass

    def hello(self):
        time.sleep(5)
        print("Hello, Junk!")

    def number(self) -> int:
        return 42


print("Initializing science.pack.junk")
for _ in tqdm(range(10)):
    time.sleep(0.1)
print("Done initializing science.pack.junk")