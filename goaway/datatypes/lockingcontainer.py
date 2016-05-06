import threading


class LockingContainer(object):
    """A context manager that wraps a single value in a threadsafe lock."""
    def __init__(self, value):
        self._lock = threading.RLock()
        self._value = value

    def replace(self, value):
        """Replace the contained value.
        This is a thread-safe operation.
        """
        with self._lock:
            self._value = value

    def __enter__(self):
        self._lock.acquire()
        return self._value

    def __exit__(self, exc_type, exc_value, traceback):
        self._lock.release()
        return False


if __name__ == "__main__":
    # Example usage.
    menu_locked = LockingContainer({})

    with menu_locked as menu:
        menu["eggs"] = "1 dolla"
        print menu

    menu_locked.replace({"nevermind": "we're closed"})

    with menu_locked as menu:
        print menu
