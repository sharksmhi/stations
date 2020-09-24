# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-09-24 16:16

@author: a002028

"""
import os
from pathlib import Path
from readers.yml import yaml_reader


class Settings(object):
    """
    """
    def __init__(self):
        self.base_directory = os.path.dirname(os.path.realpath(__file__))
        etc_path = os.path.join(self.base_directory, 'etc')
        self._load_settings(etc_path)

    def __setattr__(self, name, value):
        """
        Defines the setattr for object self
        :param name: str
        :param value: any kind
        :return:
        """
        # if anything here: do something else: delete def
        super().__setattr__(name, value)

    def _load_settings(self, etc_path):
        """
        :param etc_path: str, local path to settings
        :return: Updates attributes of self
        """
        paths = self.generate_filepaths(etc_path, pattern='.yaml')
        settings = {}
        for path in paths:
            data = yaml_reader(path)
            settings.setdefault(Path(path).stem, data)

        self.set_attributes(self, **settings)

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

    @staticmethod
    def generate_filepaths(directory, pattern=''):
        """
        #TODO Move to utils?
        :param directory: str, directory path
        :param pattern: str
        :return: generator
        """
        for path, subdir, fids in os.walk(directory):
            for f in fids:
                if pattern in f:
                    yield os.path.abspath(os.path.join(path, f))


if __name__ == '__main__':

    settings = Settings()
