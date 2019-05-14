import logging
import inspect
import warnings
import sys

try:
    from django.conf import settings as dsettings

    is_django = True
except ImportError:
    warnings.warn("Unable to import Django", ImportWarning)
    is_django = False


DECMODE = (("calling", 0), ("decorating", 1))


class DebugDecorator:
    """Functions as a base for debugging decorators."""

    def __init__(self, func, logger=None, log_handler=None, log_format=None):
        """
        Parameters
        ----------
        func : function
            The function to be decorated
        logger : logging.Logger
            A logging object to be used as a log, if not, it will create a default
            logger with with a DEBUG log level
        log_handler : logging.Handler
            A custom log handler, if not, it defaults to StreamHandler with stdout as the output
        log_format : str
            A custom log format, if not is specified, it defaults to '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        Returns
        -------
        None
        """
        self.func = func

        self.logger = logger
        if not self.logger:
            logging.basicConfig(level=logging.DEBUG)
            self.logger = logging.getLogger(__name__)

        if not log_handler:
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(logging.DEBUG)

            formatter = logging.Formatter(
                log_format or "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        else:
            self.logger.addHandler(log_handler)

        self.mode = DECMODE[1]  # decorating

    def raise_if_not_callable(self):
        """
        Parameters
        ----------
        self : Decorated
            The self's class object

        Returns
        -------
        bool
            returns True of False if the given function is callable.
        """

        if not callable(self.func):
            raise TypeError(f"{self.func.__name__!r} object is not callable")
        return True

    def setup(self, *args, **kwargs):
        """
        Setup the debugging functions to be done

        Parameters
        ----------
        *args - tuple
            The args to be passed to the function to be decorated
        **kwargs - tuple
            The kwargs to be passed to the function to be decorated

        Returns
        -------
        setup() should not return anything
        """

        raise NotImplemented()

    def debug_func(self, *args, **kwargs):
        """
        debug_func get's called to decorate the given function

        Parameters
        ----------
        *args - tuple
            The args to be passed to the function to be decorated
        **kwargs - tuple
            The kwargs to be passed to the function to be decorated

        Returns
        -------
        debug_func() should return the returned code/object of the decorated
        function
        """

        raise NotImplemented()

    def cleanup(self, result=None, *args, **kwargs):
        """
        cleanup() get's called to cleanup anything that setup() has created

        Parameters
        ----------
        results : object
            The returned result of debug_func.
        *args - tuple
            The args to be passed to the function to be decorated
        **kwargs - tuple
            The kwargs to be passed to the function to be decorated

        Returns
        -------
        cleanup() should not return anything
        """
        raise NotImplemented()

    def __call__(self, *args, **kwargs):
        """
        Get's called then a function is decorated

        Parameters
        ----------
        *args - tuple
            The args to be passed to the function to be decorated
        **kwargs - tuple
            The kwargs to be passed to the function to be decorated

        Returns
        -------
        The result from the decorated function, which is returned by debug_func()
        """

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
        """
        Check if the current function is a class

        Returns
        -------
        bool:
            True or False if the decorated object is a class
        """

        return inspect.isclass(self.func)

    @property
    def is_func(self):
        """
        Check if the current function is a function

        Returns
        -------
        bool:
            True or False if the decorated object is a function
        """
        return inspect.isfunction(self.func)

    @property
    def is_subcls(self):
        """
        Check if the current function is a subclass of this class

        Returns
        -------
        bool:
            True or False if the decorated object is a function
        """
        try:
            return issubclass(self.func, self)
        except:
            return False
