# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-09-24 16:16

@author: a002028

"""
import os


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

    def _check_for_paths(self, dictionary):
        """
        Since default path settings are set to sirena base folder
        we need to add that base folder to all paths
        :param dictionary: Dictionary with paths as values and keys as items..
        :return: Updates dictionary with local path (self.dir_path)
        """
        for item, value in dictionary.items():
            if isinstance(value, dict):
                self._check_for_paths(value)
            elif 'path' in item:
                dictionary[item] = os.path.join(self.base_directory, value)

    def _load_settings(self, etc_path):
        """
        :param etc_path: str, local path to settings
        :return: Updates attributes of self
        """
        paths = self.generate_filepaths(etc_path, pattern='.yaml')
        settings = YAMLreader().load_yaml(paths, file_names_as_key=True, return_dict=True)
        self.set_attributes(self, **settings)
        subdirectories = self.get_subdirectories(etc_path)

        for subdir in subdirectories:
            subdir_path = '/'.join([etc_path, subdir, ''])
            paths = self.get_filepaths_from_directory(subdir_path)
            sub_settings = YAMLreader().load_yaml(paths,
                                                  file_names_as_key=True,
                                                  return_dict=True)
            self._check_for_paths(sub_settings)
            self._set_sub_object(subdir, sub_settings)

    def _load_server_info(self):
        """
        :return:
        """
        settings = JSONreader().load_json(config_files=[self.settings['paths'].get('server_info_path')],
                                          return_dict=True)
        self.set_attributes(self, **settings)

    def set_reader(self, reader):
        """
        :param reader: str
        :return: Includes reader kwargs as attributes to self
        """
        self.set_attributes(self, **self.readers[reader])

    def set_writer(self, writer=None):
        """
        :param writer: str
        :return: Includes writer kwargs as attributes to self
        """
        self.set_attributes(self, **self.writers.get(writer))

    def _set_sub_object(self, attr, value):
        """
        :param attr: str, attribute
        :param value: any kind
        :return: Updates attributes of self
        """
        setattr(self, attr, value)

    @staticmethod
    def set_attributes(obj, **kwargs):
        """
        #TODO Move to utils?
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

    @staticmethod
    def get_subdirectories(directory):
        """
        #TODO Move to utils?
        :param directory: str, directory path
        :return: list of existing directories (not files)
        """
        return [subdir for subdir in os.listdir(directory)
                if os.path.isdir(os.path.join(directory, subdir))]

    @staticmethod
    def get_filepaths_from_directory(directory):
        """
        #TODO Move to utils?
        :param directory: str, directory path
        :return: list of files in directory (not sub directories)
        """
        return [''.join([directory, fid]) for fid in os.listdir(directory)
                if not os.path.isdir(directory+fid)]


if __name__ == '__main__':

    settings = Settings()
