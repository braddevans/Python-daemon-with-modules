import datetime as dt
from scheduler.asyncio import Scheduler
from scheduler import trigger
from loguru import logger

class SchedulerUtil:
    def __init__(self, loop):
        self.scheduler = Scheduler(loop=loop)

    def get_scheduler(self):
        return self.scheduler

    def schedule_from_config(self, config, func):
        logger.info("Scheduling from config...")
        logger.info(f"[{config['name']}] every {config['timer_value']} {config['timer_type']}")

        # split MM:DD HH:MM:SS
        dt_parts = config["timer_value"].split(" ")

        date_parts = dt_parts[0].split(":")
        time_parts = dt_parts[1].split(":")

        # get month, day, year
        month = int(date_parts[0])
        day = int(date_parts[1])

        # get hours, minutes, seconds
        hours = int(time_parts[0])
        minutes = int(time_parts[1])
        seconds = int(time_parts[2])

        if config["timer_type"] == "seconds":
            self.scheduler.cyclic(dt.timedelta(seconds=seconds), func)
        elif config["timer_type"] == "minutes":
            self.scheduler.minutely(dt.time(second=seconds), func)
        elif config["timer_type"] == "hourly":
            self.scheduler.hourly(dt.time(minute=minutes, second=seconds), func)
        elif config["timer_type"] == "daily":
            self.scheduler.daily(dt.time(hours=hours, minutes=minutes), func)
        elif config["timer_type"] == "weekly":
            trigger_value = dt.time(hour=hours, minute=minutes, second=seconds)
            if day == 1:
                self.scheduler.weekly(trigger.Monday(trigger_value), func)
            elif day == 2:
                self.scheduler.weekly(trigger.Tuesday(trigger_value), func)
            elif day == 3:
                self.scheduler.weekly(trigger.Wednesday(trigger_value), func)
            elif day == 4:
                self.scheduler.weekly(trigger.Thursday(trigger_value), func)
            elif day == 5:
                self.scheduler.weekly(trigger.Friday(trigger_value), func)
            elif day == 6:
                self.scheduler.weekly(trigger.Saturday(trigger_value), func)
            elif day == 7:
                self.scheduler.weekly(trigger.Sunday(trigger_value), func)