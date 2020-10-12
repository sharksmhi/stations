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

    def validate_list(self, *args, **kwargs):
        """
        :param args:
            Expects:
                list_name(s)
        :param kwargs:
            Addition:
                validator_list
        :return:
        """
        validator_list = kwargs.get('validator_list') or self.settings.validators_sorted
        for list_name in args:
            for validator_name in validator_list:
                validator = self.settings.load_validator(validator_name)
                validator.validate(self.lists.select(list_name))

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
        assert 'reader' in kwargs
        assert args

        reader = self.settings.load_reader(kwargs.get('reader'))
        list_name = kwargs.get('list_name')
        for pop_key in ('list_name', 'reader'):
            kwargs.pop(pop_key)

        lst = reader.read(*args, **kwargs)

        self.lists.append_new_list(
            name=list_name,
            meta=reader.get('meta'),
            data=lst,
            attributes=self.settings.attributes,
        )

    def write_list(self, *args, **kwargs):
        """
        :param args: tuple
        :param kwargs: dict.
            Expects:
                writer
                list_name or list_names or data
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

        lst = kwargs.get('data') or self.lists.select(kwargs.get('list_name') or kwargs.get('list_names'))

        print('Writing stations to: %s' % file_path)
        writer.write(file_path, lst)
        print('Writer done!')


if __name__ == '__main__':
    app = App()
    app.read_list(
        'C:/Arbetsmapp/config/station.txt',
        header=0,
        sep='\t',
        encoding='cp1252',
        dtype=str,
        keep_default_na=False,
        reader='shark_master',
        list_name='master',
    )

    new_stations = {
        'statn': ['Avan centroid', 'Vallviksfjärden centroid'],
        'lat_sweref99tm': ['6729995', '6782432'],
        'lon_sweref99tm': ['618965', '620581'],
    }

    app.lists.append_new_list(
        name='new_stations',
        data=new_stations,
        attributes={k: k for k in list(new_stations)}
    )

    app.validate_list('new_stations')

    app.write_list(writer='map', list_names=['master', 'new_stations'])

    # app.write_list(writer='stnreg', list_name='master')
