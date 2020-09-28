# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-09-25 16:41

@author: a002028

"""
import os
from datetime import datetime
from collections import Mapping


def generate_filepaths(directory, pattern=''):
    """
    :param directory: str, directory path
    :param pattern: str
    :return: generator
    """
    for path, subdir, fids in os.walk(directory):
        for f in fids:
            if pattern in f:
                yield os.path.abspath(os.path.join(path, f))


def get_now_time(fmt='%Y-%m-%d %H:%M:%S'):
    """
    :param fmt: str, format to export datetime object
    :return:
    """
    return datetime.now().strftime(fmt)


def recursive_dict_update(d, u):
    """ Recursive dictionary update using
    Copied from:
        http://stackoverflow.com/questions/3232943/update-value-of-a-nested-dictionary-of-varying-depth
        via satpy
    """
    for k, v in u.items():
        if isinstance(v, Mapping):
            r = recursive_dict_update(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d
