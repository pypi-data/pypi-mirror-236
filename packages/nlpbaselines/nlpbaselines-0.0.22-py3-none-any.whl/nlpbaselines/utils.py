import time
import functools
import sys
from importlib import reload


def show_gpu():
    import torch

    if torch.cuda.is_available():
        print(f"There is/are {torch.cuda.device_count()} gpus.")
        for i in range(torch.cuda.device_count()):
            print(f"the model of card {i} is {torch.cuda.get_device_name(i)}")
        print("for more info, run nvidia-smi")
    else:
        print("no gpu available")


def hello_world():
    print("hello this is nlpbaselines!")


def timer(func):
    @functools.wraps(func)
    def time_closure(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        time_elapsed = time.perf_counter() - start
        print(f"Function: {func.__name__}, Time: {time_elapsed}")
        return result

    return time_closure


def reimport_all(package):
    reload(sys.modules[package])


def dump_pickle(obj, fn):
    """_summary_

    Args:
        obj (the object to dump): _description_
        fn (filename): _description_
    """
    import pickle

    with open(fn, "wb") as file:
        # A new file will be created
        pickle.dump(obj, file)

def read_pickle(fn):
    # read a pickle file
    import pickle
    with open(fn, 'rb') as file:
        # The protocol version used is detected automatically, so we do not
        # have to specify it.
        obj = pickle.load(file)
    return obj
