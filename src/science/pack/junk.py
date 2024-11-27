import time

from tqdm.auto import tqdm

class Junk():
    def __init__(self):
        pass

    def hello(self):
        time.sleep(5)
        print("Hello, Junk!")


print("Slowly initializing science Junk")
for _ in tqdm(range(10)):
    time.sleep(0.1)
print("Science Junk initialized")