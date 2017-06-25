from threading import Timer
from runners.price_automatically_worker import PriceAutomaticallyWorker

worker = PriceAutomaticallyWorker()

class PriceAutomaticallyRunner(object):
    def __init__(self, interval):
        self._timer     = None
        self.interval   = interval
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        worker.execute()

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False








