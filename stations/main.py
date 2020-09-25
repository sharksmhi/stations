# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-09-24 16:45

@author: a002028

"""
from stations.config import Settings
from stations.handler import List


class App:
    """
    """
    def __init__(self, *args, **kwargs):
        self.settings = Settings(**kwargs)
        self.list = List()

    def read_list(self, *args, **kwargs):
        """
        :param args: tuple
        :param kwargs: dict
        :return:
        """
        try:
            assert 'reader' in kwargs
            assert args
        except AssertionError:
            print('Warning! No reader or filepath given, hence no list loaded')
            return

        reader = self.settings.load_reader(kwargs.get('reader'))
        kwargs.pop('reader')
        lst = reader.read(*args, **kwargs)
        self.list.update_attributes(dataframe=lst,
                                    attributes=self.settings.attributes)

    def write_list(self, *args, **kwargs):
        """
        :param args: tuple
        :param kwargs: dict
        :return:
        """
        try:
            assert 'writer' in kwargs
        except AssertionError:
            print('Warning! No writer given, hence no list written')
            return

        file_path = kwargs.get('file_path') or self.settings.get_export_file_path(**kwargs)

        writer = self.settings.load_writer(kwargs.get('writer'))
        writer.write(file_path, self.list)


if __name__ == '__main__':
    app = App()
    app.read_list('C:/Arbetsmapp/config/station.txt',
                  reader='text',
                  header=0,
                  sep='\t',
                  encoding='cp1252',
                  dtype=str,
                  keep_default_na=False)

    app.write_list(writer='stnreg')
