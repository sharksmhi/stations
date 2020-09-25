# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-09-25 13:28

@author: a002028

"""
import pandas as pd
from stations.utils import get_now_time


class StnRegWriter(object):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.header = kwargs.get('header')
        self.meta_header = kwargs.get('meta_header')
        self.mapping = kwargs.get('attribute_mapping')
        self.constants = kwargs.get('attribute_constants')

    def get_metaframe(self):
        """
        :return:
        """
        mf = pd.DataFrame(columns=self.meta_header, index=[0])
        for col in self.meta_header:
            if col == 'Datum':
                mf[col] = get_now_time()
            else:
                mf[col] = self.constants.get(col) or ''

        return mf

    def write(self, file_path, list_obj):
        """
        :param list_obj:
        :return:
        """
        mf = self.get_metaframe()
        df = pd.DataFrame(columns=self.header, index=[])

        for col in self.header:
            lst_key = self.mapping.get(col)
            if lst_key and hasattr(list_obj, lst_key):
                df[col] = list_obj.get(lst_key)
            else:
                df[col] = self.constants.get(col) or ''

        self._write({'Provplatser': df,
                     'Metadata': mf},
                    file_path)

    def _write(self, dictionary, path_to_new_file):
        """
        :param dictionary:
        :param path_to_new_file:
        :return:
        """
        print('Saving stations to: %s' % path_to_new_file)
        xls = XlsxWriter(file_path=path_to_new_file)
        xls.write_multiple_sheets(dictionary)
        print('done')


class XlsxWriter:
    """
    """
    def __init__(self, **kwargs):
        self.xlsx_writer = pd.ExcelWriter(kwargs.get('file_path'), engine='openpyxl')

    def _load_xlsx_writer(self, save_path, engine='openpyxl'):
        """
        Create a Pandas Excel writer using engine.
        :param save_path: str, path to file
        :param engine: Engine for the writer
        :return: Pandas Excel writer using engine.
        """
        raise NotImplementedError

    def write_multiple_sheets(self, dictionary):
        """
        :param dictionary:
        :return:
        """
        for sheet_name, frame in dictionary.items():
            frame.to_excel(self.xlsx_writer,
                           sheet_name=sheet_name,
                           na_rep='',
                           index=False,
                           encoding='cp1252')
        self.close_writer()

    def close_writer(self):
        """
        Close the Pandas Excel writer and save the Excel file.
        :return:
        """
        self.xlsx_writer.save()
