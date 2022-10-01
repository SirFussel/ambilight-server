import pyudev
import signal
import time
import threading

class GracefulKiller:
    """
    https://stackoverflow.com/questions/18499497/how-to-process-sigterm-signal-gracefully/31464349#31464349
    """
    def __init__(self):
        self.kill_now = False
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, *args):
        self.kill_now = True

class BlindService:
    def __init__(self) -> None:
        self.devices = {}
        self._worker = threading.Thread(target=self._device_handler, daemon=True)
        self._worker.start()
        
    def _device_handler(self):
        context = pyudev.Context()
        monitor = pyudev.Monitor.from_netlink(context)
        monitor.filter_by('block')
        for device in iter(monitor.poll, None):
            if 'ID_FS_TYPE' in device:
                print('{0} partition {1}'.format(device.action, device.get('ID_FS_LABEL')))
    
    def add_device(self, device_label: str):
        self.devices.append(device_label)
    
    def remove_device(self, device_label: str):
        self.devices.remove(device_label)



# observer did not block
print("no block")
killer = GracefulKiller()

while not killer.kill_now:
    time.sleep(0.1)