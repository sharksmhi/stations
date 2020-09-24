# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-09-24 16:27

@author: a002028

"""
import pandas as pd
import numpy as np


class NumpyReaderBase(object):
    """
    """
    def __init__(self):
        super(NumpyReaderBase, self).__init__()

    @staticmethod
    def read(*args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        return np.loadtxt(*args, **kwargs)


class PandasReaderBase(object):
    """
    """
    def __init__(self):
        super(PandasReaderBase, self).__init__()

    @staticmethod
    def read(*args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        return pd.read_csv(*args, **kwargs)


class NoneReaderBase(object):
    """
    Dummy base
    """
    def __init__(self):
        super(NoneReaderBase, self).__init__()

    @staticmethod
    def read(*args, **kwargs):
        print('Warning! No shape was read due to unrecognizable datatype')


def text_reader(reader_type, *args, **kwargs):
    """
    :param reader_type:
    :param args:
    :param kwargs:
    :return:
    """
    if reader_type is 'pandas':
        base = PandasReaderBase
    elif reader_type is 'numpy':
        base = NumpyReaderBase
    else:
        base = NoneReaderBase

    class TextReader(base):
        """
        """
        def __init__(self):
            super(TextReader, self).__init__()

    tr = TextReader()
    return tr.read(*args, **kwargs)
