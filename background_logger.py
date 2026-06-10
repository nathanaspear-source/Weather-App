"""Logs weather data in the background for every city listed in config"""

import logging
import signal
import time

import config
from main import safe_weather_logger

logger = logging.getLogger(__name__)

def run_weather_cycle(cities):
    """Retrieves and logs weather data for each city once in weather.csv"""
    for city in cities:
        ok, error = safe_weather_logger(city)
        if ok:
            logger.info(f"Logged {city}")
        else:
            logger.warning(f"Failed logging {city}: {error}")

        time.sleep(config.BACKGROUND_PER_CITY_DELAY_SECONDS)

def interruptible_sleep(seconds, stop_flag):
    """Sleeps to prevent a delay in city logging when project is being run"""
    for _ in range(seconds):
        if stop_flag["stop"]:
            return
        time.sleep(1)

def main():
    logging.basicConfig(
        level = logging.INFO,
        format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    stop_flag = {"stop": False}

    def handle_signal(sig, frame):
        logger.info(f"Received signal {sig}: Shutting down...")
        stop_flag["stop"] = True

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    logger.info(
        f"Starting background logger for {len(config.CITIES)} cities every {config.BACKGROUND_LOG_INTERVAL_SECONDS} seconds"
    )

    while not stop_flag["stop"]:
        run_weather_cycle(config.CITIES)
        interruptible_sleep(config.BACKGROUND_LOG_INTERVAL_SECONDS, stop_flag)

    logger.info("Background logger finished")

if __name__ == "__main__":
    main()
