# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-09-24 16:16

@author: a002028

"""
import os
from pathlib import Path
from stations.readers.yml import yaml_reader
from stations.utils import generate_filepaths, recursive_dict_update


class SettingsBase:
    def __init__(self, *args, **kwargs):
        super(SettingsBase, self).__init__()
        self.default_attributes = None
        self.readers = {}
        self.writers = {}

    def __setattr__(self, name, value):
        """
        Defines the setattr for object self.
        Special management of readers and writers.
        :param name: str
        :param value: any kind
        :return:
        """
        if os.path.isfile(name):
            if isinstance(value, dict) and ('readers' in name or 'writers' in name):
                if 'readers' in name:
                    recursive_dict_update(self.readers, {Path(name).stem: value})
                else:
                    recursive_dict_update(self.writers, {Path(name).stem: value})
            else:
                super().__setattr__(Path(name).stem, value)
        elif name == 'attributes':
            super().__setattr__(name, self._get_attribute_dictionary(value))
        else:
            super().__setattr__(name, value)

    @staticmethod
    def _get_attribute_dictionary(settings_attributes):
        """
        :param settings_attributes:
        :return:
        """
        d = {}
        for key, item in settings_attributes.items():
            if isinstance(item, str):
                d.setdefault(item, key)
            elif isinstance(item, list):
                for attrb in item:
                    d.setdefault(attrb, key)
            else:
                raise Warning('Type of item is nor str or list:', type(item))
        return d

    def set_attributes(self, **kwargs):
        """
        :param kwargs: Dictionary
        :return: sets attributes to object
        """
        for key, value in kwargs.items():
            setattr(self, key, value)


class Settings(SettingsBase):
    """
    """
    def __init__(self, *args, **kwargs):
        super(Settings, self).__init__()
        self.base_directory = os.path.dirname(os.path.realpath(__file__))
        etc_path = os.path.join(self.base_directory, 'etc')
        self._load_settings(etc_path)

        self.attributes = kwargs.get('attributes') or self.default_attributes

    def _load_settings(self, etc_path):
        """
        Loading all .yaml files from etc directory.
        Special handling of readers and writers (see SettingsBase.__setattr__())
        :param etc_path: str, local path to settings
        :return: Updates attributes of self
        """
        paths = generate_filepaths(etc_path, pattern='.yaml')
        etc_data = {}
        for path in paths:
            data = yaml_reader(path)
            etc_data.setdefault(path, data)

        self.set_attributes(**etc_data)

    def load_reader(self, reader):
        """
        :param reader: str, given by user
        :return:
        """
        reader_instance = self.readers[reader].get('reader')
        return reader_instance(**self.readers.get(reader))

    def load_writer(self, writer):
        """
        :param writer: str, given by user
        :return:
        """
        writer_instance = self.writers[writer].get('writer')
        return writer_instance(**self.writers.get(writer))

    def get_export_file_path(self, **kwargs):
        """
        Whenever there is not a export path given by the user, we try to export elsewhere..
        :return:
        """
        if kwargs.get('file_path'):
            if os.path.isdir(kwargs.get('file_path')):
                return kwargs.get('file_path')
            else:
                raise Warning('file_path given, but it´s not valid.')

        target_path = 'C:/station_exports'
        if os.path.isdir('C:/'):
            if not os.path.isdir(target_path):
                os.mkdir(target_path)
        else:
            target_path = self.base_directory

        file_name = kwargs.get('file_name') or kwargs.get('default_file_name')

        return os.path.join(target_path, file_name)


if __name__ == '__main__':

    settings = Settings()
