# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-09-25 13:43

@author: a002028

"""
import pandas as pd


class ListBase(object):
    """
    """
    def __init__(self):
        super(ListBase, self).__init__()
        self.boolean = True

    def __setattr__(self, name, value):
        """
        Defines the setattr for object self
        :param name: str
        :param value: any kind
        :return:
        """
        # if anything here: do something else: delete def
        super().__setattr__(name, value)

    @staticmethod
    def set_attributes(obj, **kwargs):
        """
        With the possibility to add attributes to an object which is not 'self'
        :param obj: object
        :param kwargs: Dictionary
        :return: sets attributes to object
        """
        for key, value in kwargs.items():
            setattr(obj, key, value)


class List(ListBase):
    """
    """
    def __init__(self):
        super(List, self).__init__()

    def get(self, item):
        """
        :param item: str
        :return:
        """
        if item in self.__dict__.keys():
            return self.__getattribute__(item)
        else:
            print('Warning! Can´t find attribute named: %s' % item)
            return None

    def update_attributes(self, *args, **kwargs):
        """
        :param args: tuple
        :param kwargs: dict
            Expects:
                dataframe or dictionary
                attributes
        :return:
        """
        if 'dataframe' in kwargs:
            data = kwargs.get('dataframe')
        elif 'dictionary' in kwargs:
            data = kwargs.get('dictionary')
        else:
            data = ()
        try:
            assert len(data)
        except AssertionError:
            print('No data given..')
            return

        try:
            assert 'attributes' in kwargs
            attrbs = kwargs.get('attributes')
        except AssertionError:
            print('No attributes given..')
            return

        dictionary = {a: pd.Series(data[key]) for a, key in attrbs.items() if key in data}

        self.set_attributes(self, **dictionary)
