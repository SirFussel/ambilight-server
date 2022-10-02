import signal


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