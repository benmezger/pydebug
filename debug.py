import inspect
import logging
import functools
import sys
import time
import dis
import cProfile
import pstats
import os
import errno

try:
    from django.conf import settings as dsettings
    is_django = True
except ImportError:
    dsettings = {}
    is_django = False

try:
    from ipdb import runcall
except ImportError:
    from pdb import runcall

try:
    from line_profiler import LineProfiler
    has_line_profiler = True
except ImportError:
    has_line_profiler = False

class DebugDecorator:
    def __init__(self, func, logger=None):
        self.func = func

        self.logger = logger
        if not self.logger:
            self.logger = logging.getLogger()

        self.mode = 1  # decorating
        self.sys_version = sys.executable

    def raise_if_not_callable(self):
        if not callable(self.func):
            raise TypeError(f"{self.func.__name__!r} object is not callable")
        return True

    def setup(self, *args, **kwargs):
        """ Setup the debugging functions to be done """
        raise NotImplemented()

    def debug_func(self, *args, **kwargs):
        """ the function """
        raise NotImplemented()

    def cleanup(self, result=None, *args, **kwargs):
        """ Cleanup any debugging functions """
        raise NotImplemented()

    def __call__(self, *args, **kwargs):
        if self.mode == "decorating":
            self.func = args[0]
            self.mode = 1  # calling mode
            return self

        # we ignore if it's a subclass
        if self.is_subcls:
            print(self.func)
            return self.func(*args, **kwargs)

        # Ignore if it's a Django project and debug is set to False
        if is_django and not dsettings.get("DEBUG"):
            return self.func(*args, **kwargs)

        self.setup(*args, **kwargs)
        result = self.debug_func(*args, **kwargs)
        self.cleanup(result=None, *args, **kwargs)

        return result

    @property
    def is_class(self):
        return inspect.isclass(self.func)

    @property
    def is_func(self):
        return inspect.isfunction(self.func)

    @property
    def is_subcls(self):
        try:
            return issubclass(self.func, self)
        except:
            return False


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


class PDBDebugger(DebugDecorator):
    def __init__(self, logger=None):
        super().__init__(logger)

    def setup(self, *args, **kwargs):
        pass

    def cleanup(self, *args, **kwargs):
        pass

    def debug_func(self, *args, **kwargs):
        return runcall(self.func, *args, **kwargs)


class DisassembleDebug(DebugDecorator):
    def __init__(self, logger=None):
        super().__init__(logger)

    def setup(self, *args, **kwargs):
        pass

    def cleanup(self, *args, **kwargs):
        pass

    def debug_func(self, *args, **kwargs):
        print(dis.dis(self.func))
        return self.func(*args, **kwargs)


class ProfilerDebug(DebugDecorator):
    def __init__(self, logger=None, profiler_log="profiler.out", delete_after=True):
        super().__init__(logger)
        self.profiler_log = profiler_log
        self.delete_after = delete_after

    def setup(self, *args, **kwargs):
        self.prof = cProfile.Profile()

    def cleanup(self, *args, **kwargs):
        if not self.delete_after:
            return

        try:
            os.remove(self.profiler_log)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise  # re-raise exception if a different error occurred
            return

    def debug_func(self, *args, **kwargs):
        self.prof.enable()

        ret = self.func(*args, **kwargs)

        self.prof.disable()

        ps = pstats.Stats(
            self.prof, stream=sys.stdout
        )  # Change this to use profiler_log later
        ps.print_stats()
        ps.print_callees()
        ps.print_callers()
        return ret


class LineProfilerDebug(DebugDecorator):
    def __init__(self, logger=None):
        super().__init__(logger)

    def setup(self, *args, **kwargs):
        if not has_line_profiler:
            raise ImportError("'line_profiler' not found.")

        self.lprof = LineProfiler()

    def cleanup(self, *args, **kwargs):
        pass

    def debug_func(self, *args, **kwargs):
        self.lprof.add_function(self.func)
        self.lprof.enable_by_count()

        ret = self.func(*args, **kwargs)
        self.lprof.print_stats()

        return ret


if __name__ == "__main__":

    @LineProfilerDebug
    def hello(a, b):
        for i in range(10000):
            os.path.exists("/etc/")
        x = 12
        print("DONE")
        return (a, b)

    hello(1, 2)
