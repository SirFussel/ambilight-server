import time
import threading
from base import GracefulKiller
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


class BlindService:
    def __init__(self) -> None:
        # Create the I2C bus
        self.i2c = busio.I2C(board.SCL, board.SDA)
        # Create the ADC object using the I2C bus
        self.ads = ADS.ADS1015(self.i2c)
        # Create single-ended input on channel 0
        self.chan = AnalogIn(self.ads, ADS.P0)

        self._worker = threading.Thread(target=self._poll, daemon=True)
        self._worker.start()
        
    def _poll(self):
        print("{:>5}\t{:>5}".format('raw', 'v'))
        while True:
            print("{:>5}\t{:>5.3f}".format(self.chan.value, self.chan.voltage))
            time.sleep(0.5)

# observer did not block
print("no block")
killer = GracefulKiller()

while not killer.kill_now:
    time.sleep(0.1)