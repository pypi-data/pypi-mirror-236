import time


class timer:
    def __init__(self) -> None:
        self.time_start = 0
        pass

    def reset(self):
        self.time_start = time.time()
        return 0

    def get(self):
        period = time.time() - self.time_start
        return period
