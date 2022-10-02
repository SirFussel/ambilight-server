#!/usr/bin/python3
import RPi.GPIO as GPIO
import re
import os
import logging
from datetime import datetime
import sys
import time
from base import GracefulKiller


class TemperatureControl:
    def __init__(self, write_logs: bool = False):
        self._killer = GracefulKiller()

        self.TEMP_UPPER_LIMIT_CELSIUS = 55.0
        self.TEMP_LOWER_LIMIT_CELSIUS = 48.0

        self.cpu_temp: float = 0.0
        self.last_cpu_temp: float = 0.0
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        stdout_handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        stdout_handler.setFormatter(formatter)
        self.logger.addHandler(stdout_handler)

        if write_logs:
            log_dir = os.path.join(os.getcwd(), "logs")
            os.makedirs(log_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%y-%m-%d_%H-%M-%S")
            log_location = os.path.join(log_dir, f"{timestamp}.log")
            output_file_handler = logging.FileHandler(log_location)
            output_file_handler.setFormatter(formatter)
            self.logger.addHandler(output_file_handler)
            self.logger.info(f"Writing logs to {log_location}")
        else:
            self.logger.info("Writing logs disabled")
        self.logger.info("Configuring board settings")
        self.fan_pin = 17
        self.fan_enabled = False
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.fan_pin, GPIO.OUT)
        self.disable_fan()

    def get_temperature(self) -> float:
        try:
            cpu_temp_str = os.popen("vcgencmd measure_temp").readline()
            return float(re.sub(r"[^0-9.]+", "", cpu_temp_str))
        except Exception as e:
            self.logger.exception("An error occurred while reading temperature:", exc_info=e)

    def enable_fan(self):
        try:
            GPIO.output(self.fan_pin, True)
            self.fan_enabled = True
            self.logger.info("Fan enabled")
        except Exception as e:
            self.logger.exception("Failed to enable fan:", exc_info=e)

    def disable_fan(self):
        try:
            GPIO.output(self.fan_pin, False)
            self.fan_enabled = False
            self.logger.info("Fan disabled")
        except Exception as e:
            self.logger.exception("Failed to enable fan:", exc_info=e)

    def run(self):
        try:
            while not self._killer.kill_now:
                self.last_cpu_temp = self.cpu_temp
                self.cpu_temp = self.get_temperature()
                self.logger.info(f"Current cpu temperature {self.cpu_temp} \'C")
                if self.cpu_temp >= self.TEMP_UPPER_LIMIT_CELSIUS:
                    if not self.fan_enabled:
                        self.logger.info(f"Temperature limit of {self.TEMP_UPPER_LIMIT_CELSIUS} \'C exceeded")
                        self.enable_fan()
                elif self.cpu_temp <= self.TEMP_LOWER_LIMIT_CELSIUS:
                    if self.fan_enabled:
                        self.logger.info(f"Temperature fell below limit of {self.TEMP_LOWER_LIMIT_CELSIUS} \'C")
                        self.disable_fan()
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("User requested exit.")
            sys.exit(0)
        except Exception as e:
            self.logger.exception("Unhandled error:", exc_info=e)
        finally:
            GPIO.cleanup()


if __name__ == "__main__":
    tc = TemperatureControl()
    tc.run()
