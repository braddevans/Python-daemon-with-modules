import os
import sys
import asyncio

from loguru import logger

from Utils.scheduler_util import SchedulerUtil
from Utils.utils_py import init_config
from daemon_loaders import init_modules

# init Variables
logger.remove()
logger.add(sys.stdout, format="<blue>[{time:YYYY-MM-DD HH:mm:ss!UTC}]</blue> [{file}:{line}] <level>{message}</level>")

async def main():
    loop = asyncio.get_running_loop()
    config = init_config() # unused variable but init's the default config.json
    logger_config = config.get("logger", {})
    logger.add(
        "logs/daemon.log",
        rotation=logger_config.get("rotation", "10 MB"),
        compression=logger_config.get("compression", "zip"),
        retention=logger_config.get("retention", "15 days"),
        format="<blue>[{time:YYYY-MM-DD HH:mm:ss!UTC}]</blue> [{file}:{line}] <level>{message}</level>"
    )

    sheduler_util = SchedulerUtil(loop)
    shared_context = {"logger": logger, "sheduler_util": sheduler_util}
    sheduler = sheduler_util.get_scheduler() # unused variable

    await init_modules(shared_context)

    try:
        logger.info("Starting Daemon...")
        while True:
            await asyncio.sleep(1)


    except asyncio.CancelledError as e:  # instead of KeyboardInterrupt
        logger.error(f"[asyncio.CancelledError]: {e}")
        os._exit(167)

if __name__ == "__main__":
    asyncio.run(main())