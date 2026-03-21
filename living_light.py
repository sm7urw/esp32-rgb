import time
import threading

# Configuration Constants
PWM_FREQUENCY = 1000  # PWM frequency in Hertz
DEBOUNCE_TIME = 200  # Debounce time in milliseconds

# Thread-safe mechanism to handle concurrent access
class ThreadSafe:
    def __init__(self):
        self.lock = threading.Lock()

    def execute(self, function, *args, **kwargs):
        with self.lock:
            return function(*args, **kwargs)

# Improved class with debounce and proper frequency management
class LivingLight:
    def __init__(self):
        self.is_on = False
        self.thread_safe = ThreadSafe()

    def set_light(self, state):
        # Debouncing logic
        time.sleep(DEBOUNCE_TIME / 1000.0)  # Convert milliseconds to seconds
        self.thread_safe.execute(self._set_light, state)

    def _set_light(self, state):
        self.is_on = state
        # Configure PWM frequency here
        print(f"Light {'on' if state else 'off'} at {PWM_FREQUENCY} Hz.")

# Example usage
if __name__ == '__main__':
    light = LivingLight()
    light.set_light(True)  # Turn light on
    time.sleep(1)  # Keep it on for 1 second
    light.set_light(False)  # Turn light off