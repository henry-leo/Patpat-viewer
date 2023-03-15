global PATPAT_ENV


def _init():
    global PATPAT_ENV
    PATPAT_ENV = None


def set_env(env=None):
    global PATPAT_ENV
    PATPAT_ENV = env


def get_env():
    global PATPAT_ENV
    if PATPAT_ENV is None:
        PATPAT_ENV = './patpat_env'
    return PATPAT_ENV


_init()
