#%%
from queue import Queue
from threading import Thread
import time


def get_fib():
    return "this is fib."


class DataLoggingThread(Thread):
    def __init__(self, name: str, queue: Queue):
        super(DataLoggingThread, self).__init__()
        self.name = name
        self.queue = queue

    def run(self):
        print(f"<{self.name}> running...")

        local_temp = get_fib()
        
        print(f"local_temp: {repr(local_temp)}")
        # print(f"Queue `{repr(content)}` done")
        # content = self.queue.get()
        # self.queue.task_done()


if "__main__" == __name__:
    DataLoggingQueue = Queue(-1)

    t = DataLoggingThread("Error Data Logging", DataLoggingQueue)
    t.start()

    # time.sleep(5)

    for i in range(5):
        print("Queue inputing")
        DataLoggingQueue.put(f"i nef:: {i}\n")
        if i == 2:
            print("Main sleeping")
            time.sleep(5)

# %%
