import logging
import inspect
import warnings

try:
    from django.conf import settings as dsettings
    is_django = True
except ImportError:
    warnings.warn("Unable to import Django", ImportWarning)
    is_django = False


DECMODE = (('calling', 0), ('decorating', 1))

class DebugDecorator:
    def __init__(self, func, logger=None):
        self.func = func

        self.logger = logger
        if not self.logger:
            self.logger = logging.getLogger()

        self.mode = DECMODE[1]  # decorating

    def raise_if_not_callable(self):
        if not callable(self.func):
            raise TypeError(f"{self.func.__name__!r} object is not callable")
        return True

    def setup(self, *args, **kwargs):
        """ Setup the debugging functions to be done """
        raise NotImplemented()

    def debug_func(self, *args, **kwargs):
        """ the function to be ran"""
        raise NotImplemented()

    def cleanup(self, result=None, *args, **kwargs):
        """ Cleanup any debugging functions """
        raise NotImplemented()

    def __call__(self, *args, **kwargs):
        if self.mode == DECMODE[1]:
            self.func = args[0]
            self.mode = DECMODE[0]  # calling mode
            return self

        # we ignore if it's a subclass
        if self.is_subcls:
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
