import time

from .base import DebugDecorator


class ObjectInfoDebug(DebugDecorator):
    def __init__(self, logger=None):
        super().__init__(logger)

    def setup(self, *args, **kwargs):
        self.args_repr = (repr(a) for a in args)
        self.kwargs_repr = (f"{k}={v!r}" for k, v in kwargs.items())
        self.signature = ", ".join(list(self.args_repr) + list(self.kwargs_repr))

    def cleanup(self, *args, **kwargs):
        pass

    def debug_func(self, *args, **kwargs):
        perf_start = time.perf_counter()
        proc_start = time.process_time()

        ret = self.func(*args, **kwargs)

        total_perf = (time.perf_counter() - perf_start) / 60
        total_proc = (time.process_time() - proc_start) / 60

        name = self.func.__name__ if self.is_func else self.func.__class__.__name__
        if self.is_func:
            print(f"Calling {name}({self.signature})")
            print(f"{name!r} Elapsed time: {total_perf} [min]")
            print(f"{name!r} CPU process time: {total_proc} [min]")
            print(f"{name!r} returned {ret!r}")
        else:
            print(f"Calling {name}({self.signature})")
            print(f"{name!r} Elapsed time: {total_perf} [min]")
            print(f"{name!r} CPU process time: {total_proc} [min]")
            print(f"{name!r} returned {ret!r}")

        return ret
