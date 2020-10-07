# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-09-25 13:43

@author: a002028

"""
import pandas as pd


class Meta(dict):
    """
    """
    def __init__(self, *args, **kwargs):
        self.args = [a for a in args]
        for key, item in kwargs.items():
            self.setdefault(key, item)


class ListBase:
    """
    """
    def __init__(self, **kwargs):
        super(ListBase, self).__init__()
        self.loaded_attributes = []
        self.boolean = True
        self.name = None
        self.meta = None

    def __setattr__(self, name, value):
        """
        Defines the setattr for object self
        :param name: str
        :param value: any kind
        :return:
        """
        # if anything here: do something else: delete def
        if name == 'meta' and not value:
            value = {}
        super().__setattr__(name, value)

    def set_attributes(self, **kwargs):
        """
        :param obj: object
        :param kwargs: Dictionary
        :return: sets attributes to object
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
            self.loaded_attributes.append(key)


class List(ListBase):
    """
    """
    def __init__(self, **kwargs):
        super(List, self).__init__()
        for key, item in kwargs.items():
            if key == 'meta':
                if not item or item == 'None':
                    item = {}
                item = Meta(**item)
            setattr(self, key, item)

    def get(self, item, boolean=False):
        """
        :param item:
        :param boolean:
        :return:
        """
        if item in self.__dict__.keys():
            if boolean:
                return self.__getattribute__(item)[self.boolean]
            else:
                return self.__getattribute__(item)
        else:
            print('Warning! Can´t find attribute: %s' % item)
            return ''
            # return None
            # return 'None'

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

        self.set_attributes(**dictionary)

    def update_attribute_values(self, attr, values):
        """
        :param attr:
        :param values:
        :return:
        """
        self.__getattribute__(attr)[self.boolean] = values

    def set_standard_formats(self, dictionary):
        """
        :param dictionary:
        :return:
        """
        for key, item in self.meta.items():
            if key == 'synonym_separator' and 'synonyms' in dictionary:
                dictionary['synonyms'] = dictionary['synonyms'].str.replace(item, ';')

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
            self.setdefault(name, List(meta=kwargs.get('meta')))
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
            print(list_names)
            return self[list_names]


if __name__ == '__main__':
    meta = Meta('hej', 'svej', hej=44, svej=55)
    print(meta.get('hej'))
    print(meta.args)
