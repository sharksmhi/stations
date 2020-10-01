# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-09-25 13:43

@author: a002028

"""
import pandas as pd


class ListBase:
    """
    """
    def __init__(self):
        super(ListBase, self).__init__()
        self.boolean = True
        self.name = None
        self.loaded_attributes = []

    def __setattr__(self, name, value):
        """
        Defines the setattr for object self
        :param name: str
        :param value: any kind
        :return:
        """
        # if anything here: do something else: delete def
        self.loaded_attributes.append(name)
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
            print('Warning! Can´t find attribute: %s' % item)
            return 'None'

    def update_attributes(self, *args, **kwargs):
        """
        :param args: tuple
        :param kwargs: dict
            Expects:
                data as dataframe or dictionary
                attributes
        :return:
        """
        if 'data' in kwargs:
            data = kwargs.get('data')
        else:
            data = ()
        try:
            assert len(data)
        except AssertionError:
            print('No data given..')
            return

        try:
            assert 'attributes' in kwargs
            attributes = kwargs.get('attributes')
        except AssertionError:
            print('No attributes given..')
            return

        dictionary = {a: pd.Series(data[key]) for key, a in attributes.items() if key in data}

        self.set_standard_formats(dictionary)

        self.set_attributes(self, **dictionary)

    def set_standard_formats(self, dictionary):
        """
        :param dictionary:
        :return:
        """
        if 'synonyms' in dictionary:
            dictionary['synonyms'] = dictionary['synonyms'].str.replace('')

    @property
    def length(self):
        """
        :return:
        """
        return len(self.name)


class MultiList(dict):
    """
    Stores information for multiple lists.
    Uses list name as key in this dictionary of List()-objects
    """
    def append_new_list(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        name = kwargs.get('name')
        if name:
            self.setdefault(name, List())
            self[name].update_attributes(**kwargs)
        else:
            raise Warning('No list name given')

    def select(self, list_names):
        """
        :param list_names: list
        :return:
        """
        if isinstance(list_names, list):
            return {name: self[name] for name in list_names}
        else:
            return self[list_names]
