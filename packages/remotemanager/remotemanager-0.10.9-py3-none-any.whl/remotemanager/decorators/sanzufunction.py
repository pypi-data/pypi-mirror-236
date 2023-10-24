from remotemanager import Dataset


class SanzuWrapper:
    """
    Decorator class to allow you to

    Wrap a function with `@SanzuFunction` to store:

    >>> @SanzuFunction
    >>> def func(val):
    >>>     return val
    >>> func(val=3) # creates a Dataset and runs this function

    Call this function will transparently create a Dataset, execute
    the function remotely (synchronously), and return the result. The function
    must be called with explicitly named keyword arguments.
    """

    def __init__(self, function, *args, **kwargs):
        self._ds = Dataset(function=function, *args, **kwargs)

    def __call__(self, **kwargs):
        self._ds.append_run(kwargs)
        self._ds.run()
        self._ds.wait()
        self._ds.fetch_results()

        for r in self._ds.runners:
            if r.args == kwargs:
                return r.result

    @property
    def dataset(self) -> Dataset:
        """
        Return the current Dataset used for this function

        Returns:
            (Dataset): associated Dataset
        """
        return self._ds


def SanzuFunction(*args, **kwargs):
    """
    Actual decorator wrapper for SanzuFunction

    In order to make a decorator callable, Python seems to require an actual function
    call that returns the class.

    Args:
        *args:
            args to pass through to the Dataset
        **kwargs:
            kwargs to pass through to the Dataset

    Returns:
        decorator
    """
    if len(args) > 0 and hasattr(args[0], "__call__"):
        # calling the decorator with no args places the function in the first arg
        return SanzuWrapper(args[0], **kwargs)

    # Otherwise, capture the function via standard decorator
    def decorate(function):
        return SanzuWrapper(function, *args, **kwargs)

    return decorate
