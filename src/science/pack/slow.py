import time

from tqdm.auto import tqdm

class Slow():
    def __init__(self):
        pass

    def hello(self):
        time.sleep(5)
        print("Hello, Slow!")


print("Slowly initializing slow science stuff")
for _ in tqdm(range(20)):
    time.sleep(0.1)
print("Slow science stuff initialized")