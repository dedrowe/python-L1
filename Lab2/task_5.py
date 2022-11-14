from task_4 import func_next
from task_4 import read_dataset


class Iterator:
    def __init__(self):
        self.limit = len(read_dataset())
        self.count = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.count < self.limit:
            self.count += 1
            return func_next()
        else:
            raise StopIteration


if __name__ == "__main__":
    it = Iterator()
    for i in it:
        print(next(it))
