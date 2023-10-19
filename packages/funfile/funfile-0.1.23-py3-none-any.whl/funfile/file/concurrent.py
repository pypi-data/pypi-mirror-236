import time
from queue import Queue
from threading import Thread


class ConcurrentFile:
    def __init__(self, filepath, mode="w", capacity=200, timeout=3):
        self.filepath = filepath
        self.mode = mode
        self.timeout = timeout
        self._write_queue = Queue(capacity)
        self._close = False
        thread = Thread(target=self._write)
        thread.start()

    def write(self, chunk, offset=None):
        self._write_queue.put((chunk, offset))
        return len(chunk)

    def _write(self):
        with open(self.filepath, self.mode) as fw:
            while True:
                try:
                    chunk, offset = self._write_queue.get(timeout=self.timeout)
                    if offset:
                        fw.seek(offset)
                    fw.write(chunk)
                    fw.flush()
                    self._write_queue.task_done()
                except Exception as e:
                    pass
                if self._close:
                    break

    def close(self):
        self._close = True

    def wait_for_all_done(self):
        self._write_queue.join()

    def empty(self):
        return self._write_queue.empty()

    def __enter__(self):
        self._handle = self
        return self._handle

    def __exit__(self, exc_type, exc_val, exc_tb):
        while not self.empty():
            time.sleep(1)
        self.wait_for_all_done()
        self.close()
        return True
