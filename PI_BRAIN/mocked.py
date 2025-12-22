# PI_BRAIN/mocked.py

class GPIOMock:
    """A mock class to simulate RPi.GPIO."""
    
    # GPIO constants
    BCM = 11
    OUT = 1
    IN = 0
    HIGH = 1
    LOW = 0

    def __getattr__(self, name):
        """Catch-all for any method that is not explicitly defined."""
        def method(*args, **kwargs):
            print(f"[Mocked GPIO] Called: {name} with args={args} kwargs={kwargs}")
        return method

    def setmode(self, mode):
        print(f"[Mocked GPIO] Set mode to: {mode}")

    def setup(self, channel, mode, initial=None):
        print(f"[Mocked GPIO] Setup channel {channel} to mode {mode} with initial={initial}")

    def output(self, channel, value):
        print(f"[Mocked GPIO] Output to channel {channel} value: {value}")

    def input(self, channel):
        print(f"[Mocked GPIO] Input from channel {channel}")
        return 0  # Return a default value

    def cleanup(self):
        print("[Mocked GPIO] Cleanup called")

# Create an instance to be used as the mock module
GPIO = GPIOMock()
