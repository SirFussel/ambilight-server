#!/usr/bin/python3
import RPi.GPIO as GPIO
import sys
import logging
import time


class Test:
    def __init__(self):
        self.fan_pin = 17
        self.fan_enabled = False
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.fan_pin, GPIO.OUT)
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        stdout_handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        stdout_handler.setFormatter(formatter)
        self.logger.addHandler(stdout_handler)
    
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
            while True:
                self.enable_fan()
                time.sleep(5)
                self.disable_fan()
                time.sleep(5)
                
        except KeyboardInterrupt:
            GPIO.cleanup()
            self.logger.info("User requested exit.")
            sys.exit(0)
        except Exception as e:
            self.logger.exception("Unhandled error:", exc_info=e)


if __name__ == "__main__":
    tc = Test()
    tc.run()
