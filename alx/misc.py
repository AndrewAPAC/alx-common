
def singleton(cls, **kwargs):
    obj = cls(**kwargs)
    # Always return the same object
    cls.__new__ = staticmethod(lambda cls: obj, **kwargs)
    # Disable __init__
    try:
        del cls.__init__
    except AttributeError:
        pass
    return cls
