import time
from threading import Thread

import schedule


class TasksScheduler:
    def __init__(self):
        self.is_running = False

    def _observe_events(self):
        while self.is_running:
            schedule.run_pending()
            time.sleep(1)

    def stop(self):
        self.is_running = False

    def run(self):
        self.is_running = True
        thread = Thread(target=self._observe_events)
        thread.start()
