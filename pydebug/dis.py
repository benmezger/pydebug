import dis

from .base import DebugDecorator

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
