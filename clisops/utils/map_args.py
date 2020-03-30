__author__ = """Elle Smith"""
__contact__ = "eleanor.smith@stfc.ac.uk"
__copyright__ = "Copyright 2018 United Kingdom Research and Innovation"
__license__ = "BSD"
__version__ = "0.1.0"

from clisops.utils.get_data import _get_xy


def map_args(dset, **kwargs):
    args = {}

    for key, value in kwargs.items():

        if value == None:
            pass
        elif key == 'space':
            args.update(_get_xy(dset, value))
        elif key == 'level':
            pass
        else:
            args[key] = slice(value[0], value[1])

    return args
