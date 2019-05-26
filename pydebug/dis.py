import dis
import sys

from .base import DebugDecorator


class DisassembleDebug(DebugDecorator):
    def __init__(self, logger=None):
        super().__init__(logger)

    def setup(self, *args, **kwargs):
        pass

    def cleanup(self, *args, **kwargs):
        pass

    def debug_func(self, *args, **kwargs):
        if self.logger:
            logger.info(dis.dis(self.func))
        else:
            sys.stdout.write(dis.dis(self.func))

        return self.func(*args, **kwargs)
