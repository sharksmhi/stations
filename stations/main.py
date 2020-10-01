# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-09-24 16:45

@author: a002028

"""
from stations.config import Settings
from stations.handler import MultiList


class App:
    """
    """
    def __init__(self, *args, **kwargs):
        self.settings = Settings(**kwargs)
        self.lists = MultiList()

    def read_list(self, *args, **kwargs):
        """
        :param args: tuple
            Expects:
                file_path
        :param kwargs: dict
            Expects:
                reader
        :return:
        """
        try:
            assert 'reader' in kwargs
            assert args
        except AssertionError:
            print('Warning! No reader or filepath given, hence no list loaded')
            return

        reader = self.settings.load_reader(kwargs.get('reader'))
        list_name = kwargs.get('list_name')
        kwargs.pop('list_name')
        kwargs.pop('reader')
        lst = reader.read(*args, **kwargs)
        self.lists.append_new_list(name=list_name,
                                   data=lst,
                                   attributes=self.settings.attributes
                                   )

    def write_list(self, *args, **kwargs):
        """
        :param args: tuple
        :param kwargs: dict.
            Expects:
                writer
                list_name
            Addition:
                file_path
                file_name
        :return:
        """
        try:
            assert 'writer' in kwargs
        except AssertionError:
            print('Warning! No writer given, hence no list written')
            return

        writer = self.settings.load_writer(kwargs.get('writer'))
        kwargs.setdefault('default_file_name', writer.default_file_name)
        file_path = self.settings.get_export_file_path(**kwargs)

        print('Writing stations to: %s' % file_path)
        writer.write(file_path, self.lists.select(kwargs.get('list_names')))
        print('Writer done!')


if __name__ == '__main__':
    app = App()
    app.read_list('C:/Arbetsmapp/config/station.txt',
                  header=0,
                  sep='\t',
                  encoding='cp1252',
                  dtype=str,
                  keep_default_na=False,
                  reader='text',
                  list_name='master')

    new_stations = {'name': ['Avan centroid', 'Vallviksfjärden centroid'],
                    'lat_sweref99tm': ['6729995', '6782432'],
                    'lon_sweref99tm': ['618965', '620581'],
                    'lat_dd': [],
                    'lon_dd': []}
    from stations.utils import transform_ref_system

    for la, lo in zip(new_stations['lat_sweref99tm'], new_stations['lon_sweref99tm']):
        lat_dd, lon_dd = transform_ref_system(lat=la, lon=lo)
        new_stations['lat_dd'].append(round(lat_dd, 5))
        new_stations['lon_dd'].append(round(lon_dd, 5))

    app.lists.append_new_list(name='new_stations',
                              data=new_stations,
                              attributes={k: k for k in list(new_stations)}
                              )

    app.write_list(writer='map', list_names=['master'])

    # app.write_list(writer='stnreg', list_name='master')
