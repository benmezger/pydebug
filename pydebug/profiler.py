import cProfile
import pstats
import os

try:
    from line_profiler import LineProfiler

    has_line_profiler = True
except ImportError:
    warnings.warn("Unable to import line_profiler", ImportWarning)
    has_line_profiler = False

from .base import DebugDecorator


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

        if not has_line_profiler:
            raise ImportError("'line_profiler' not found.")

    def setup(self, *args, **kwargs):
        self.lprof = LineProfiler()

    def cleanup(self, *args, **kwargs):
        pass

    def debug_func(self, *args, **kwargs):
        self.lprof.add_function(self.func)
        self.lprof.enable_by_count()

        ret = self.func(*args, **kwargs)
        self.lprof.print_stats()

        return ret
