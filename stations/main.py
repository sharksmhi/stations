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
    Keep it clean, keep it tidy!
    - read
    - validate
    - write
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
                validator.validate(self.lists.select(list_name), master=self.lists.select('master'))

    def read_list(self, *args, reader=None, list_name=None, **kwargs):
        """
        :param args: tuple
            Expects:
                file_path
        :param kwargs: dict
            Expects:
                reader
        :return:
        """
        if not reader:
            raise ValueError('Missing reader! Please give one as input (App.read(reader=NAME_OF_READER)')
        if not list_name:
            raise ValueError('Missing list_name! Please give one as input (App.read(list_name=NAME_OF_LIST)')
        if not args:
            raise ValueError('Missing file path! Please give one as input (App.read(PATH_TO_DATA_SOURCE)')

        reader_kwargs = self.settings.readers[reader].get('reader_kwargs') or {}

        reader = self.settings.load_reader(reader)

        if 'reader_kwargs' in kwargs:
            for key, value in kwargs['reader_kwargs'].items():
                reader_kwargs[key] = value

        reader_kwargs = reader_kwargs or kwargs

        if reader_kwargs.get('dtype') == '':
            reader_kwargs['dtype'] = str

        lst = reader.read(*args, **reader_kwargs)

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
        writer.update_attributes(second_update=True, **kwargs)
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
        reader='shark_master',
        list_name='master',
    )

    # new_stations = {
    #     'statn': ['N Fredriksskansbron'.upper(), 'Vallviksfjärden centroid'],
    #     'lat_sweref99tm': ['6729995', '6782432'],
    #     'lon_sweref99tm': ['618965', '620581'],
    # }
    #
    # app.lists.append_new_list(
    #     name='new_stations',
    #     data=new_stations,
    #     attributes={k: k for k in list(new_stations)}
    # )

    # app.validate_list('new_stations')
    #
    # app.write_list(writer='map', list_names=['master', 'new_stations'])

    # app.write_list(writer='stnreg', list_name='new_stations')
