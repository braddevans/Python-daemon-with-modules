import time
from threading import Thread

class Example(Thread):
    def __init__(self, shared_context):
        Thread.__init__(self)
        self.daemon = True
        self.shared_context = shared_context
        self.logger = self.shared_context["logger"]
        self.thread_id = self.ident

    def run(self):
        self.logger.debug(f"[Thread: {self.ident}] Example Module is running...")
        self.logger.debug(f"[Thread: {self.ident}] Example Module Finished...")

def get_module_config():
    return {
        "name": "Example",
        "timer_type": "minutes",  # seconds, minutes, hourly, daily, weekly, monthly, yearly
        "timer_value": "00:00 00:02:00"
    }

async def init_module(shared_context):
    Example(shared_context).start()
    return True
