import math
from datastore import DataStore

db = DataStore()

def square(x):
    return x*x

def cube(x):
    return x*x*x

def sqrt(x):
    return math.sqrt(x)

def sleep(x):
    return time.sleep(x)

def grow_shared(append_string):
    """Grow a shared string.
    Appends append_string to the shared string.
    This is not an atomic operation and may lose append_string.
    """
    # The path or key is the address of the shared value.
    data_path = "tweedle_dee_value_path"
    # Ensure that the shared variable exists.
    db.create(data_path, default="")
    # Fetch the old value.
    old_value = db.get(data_path)
    # Append the argument.
    new_value = old_value + append_string
    # Save the new value to the datastore.
    db.set(data_path, new_value)
