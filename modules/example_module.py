from threading import Thread


class Example(Thread):
    def __init__(self, shared_context):
        Thread.__init__(self)
        self.daemon = True
        self.shared_context = shared_context
        self.logger = self.shared_context["logger"]
        self.thread_id = self.ident
        self.logger.add("logs/modules/Example-debug.log", filter=lambda record: "example_debug" in record["extra"])

    def run(self):
        self.logger.bind(example_debug=True).info(f"[Thread: {self.ident}] Example Module Running...")
        self.logger.bind(example_debug=True).info(f"[Thread: {self.ident}] Example Module Finished...")

def get_module_config():
    return {
        "name": "Example",
        "timer_type": "daily",  # every, timed, weekly_timed
        "timer_value": "0 07:00:00"
    }


async def init_module(shared_context):
    Example(shared_context).start()
    return True
