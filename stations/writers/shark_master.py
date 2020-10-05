# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-10-05 13:03

@author: a002028

"""
import pandas as pd
from stations.writers.writer import WriterBase


class SharkWriter(WriterBase):
    """
    """
    def __init__(self, *args, **kwargs):
        super(SharkWriter, self).__init__()
        for key, item in kwargs.items():
            setattr(self, key, item)

    def _get_dataframe(self, list_obj):
        """
        :param list_obj:
        :return:
        """
        df = pd.DataFrame(columns=self.header, index=[])

        for col in self.header:
            lst_key = self.attribute_mapping.get(col)
            if lst_key and hasattr(list_obj, lst_key):
                df[col] = list_obj.get(lst_key)
            else:
                value = self.attribute_constants.get(col) or ''
                df[col] = [value] * list_obj.length

        return df

    def write(self, file_path, list_obj):
        """
        :param file_path: str
        :param list_obj: stations.handler.List
        :return:
        """
        if isinstance(list_obj, dict):
            assert 'shark_master' in list_obj
            multiple_lists = True
        else:
            multiple_lists = False

        df_main = self._get_dataframe(list_obj['shark_master'])

        if multiple_lists:
            for list_name in list(list_obj):
                if list_name == 'shark_master':
                    continue
                df_add = self._get_dataframe(list_obj[list_name])
                df_main = df_main.append(df_add).reset_index(drop=True)

        self._write(df_main, file_path)

    def _write(self, df, path_to_new_file):
        """
        :param dictionary: dictionary
        :param path_to_new_file: str
        :return:
        """
        df.to_csv(
            path_to_new_file,
            na_rep='',
            index=False,
            encoding='cp1252',
        )
