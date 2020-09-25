# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-09-24 16:16

@author: a002028

"""
import os
from pathlib import Path
from stations.readers.yml import yaml_reader
from stations.utils import generate_filepaths


class SettingsBase(object):
    def __init__(self, *args, **kwargs):
        super(SettingsBase, self).__init__()
        self.readers = None
        self.writers = None

    def __setattr__(self, name, value):
        """
        Defines the setattr for object self
        :param name: str
        :param value: any kind
        :return:
        """
        # if anything here: do something else: delete def
        super().__setattr__(name, value)

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
        self.default_attributes = None
        self._load_settings(etc_path)

        if 'attributes' in kwargs:
            self.attributes = kwargs.get('attributes')
        else:
            self.attributes = self.default_attributes

    def _load_settings(self, etc_path):
        """
        :param etc_path: str, local path to settings
        :return: Updates attributes of self
        """
        paths = generate_filepaths(etc_path, pattern='.yaml')
        etc_data = {}
        for path in paths:
            data = yaml_reader(path)
            etc_data.setdefault(Path(path).stem, data)

        self.set_attributes(**etc_data)

    def load_reader(self, reader):
        """
        :param reader:
        :return:
        """
        reader_instance = self.readers[reader].get('reader')
        return reader_instance()

    def load_writer(self, writer):
        """
        :param writer:
        :return:
        """
        writer_instance = self.writers[writer].get('writer')
        return writer_instance(**self.writers.get(writer))

    def get_export_file_path(self, **kwargs):
        """
        Whenever there is not a export path given by the user, we try to export elsewhere..
        :return:
        """
        target_path = 'C:/export_station_list'
        if os.path.isdir('C:/'):
            if not os.path.isdir(target_path):
                os.mkdir(target_path)
        else:
            target_path = self.base_directory
        file_name = kwargs.get('file_name') or 'station_export.xlsx'

        return os.path.join(target_path, file_name)


if __name__ == '__main__':

    settings = Settings()
