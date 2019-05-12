import traceback

try:
    from ipdb import runcall
    from ipdb import launch_ipdb_on_exception

    has_ipdb = True
except ImportError:
    warnings.warn("Unable to import IPDB. Using PDB instead", ImportWarning)
    from pdb import runcall
    from pdb import Pdb

    has_ipdb = False

from .base import DebugDecorator


class PDBDebugger(DebugDecorator):
    def __init__(self, logger=None, on_error=False):
        self.on_error = on_error
        super().__init__(logger)

    def setup(self, *args, **kwargs):
        pass

    def cleanup(self, *args, **kwargs):
        pass

    def debug_func(self, *args, **kwargs):
        if not self.on_error:
            return runcall(self.func, *args, **kwargs)
        try:
            if has_ipdb:
                with launch_ipdb_on_exception():
                    return self.func(*args, **kwargs)
            else:
                return self.func(*args, **kwargs)
        except Exception as e:
            traceback.print_exc(file=sys.stderr)
            Pdb(stdin=sys.__stdin__, stdout=sys.__stdout__).set_trace()
