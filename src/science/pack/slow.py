import time

from tqdm.auto import tqdm

class Slow():
    def __init__(self):
        pass

    def hello(self):
        time.sleep(5)
        print("Hello, Slow!")

    def number(self) -> int:
        return 42000


print("Initializing science.pack.slow")
for _ in tqdm(range(20)):
    time.sleep(0.1)
print("Done initializing science.pack.slow")