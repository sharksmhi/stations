# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-10-09 17:22

@author: a002028

"""
from abc import ABC
import copy
import yaml
import pandas as pd
from stations.validators.validator import ValidatorLog
from stations.writers.writer import WriterBase


class ValidationWriter(WriterBase, ABC):
    """
    """
    def __init__(self, *args, **kwargs):
        super(ValidationWriter, self).__init__()
        self.update_attributes(**kwargs)

    @staticmethod
    def write(file_path, log):
        """
        :param file_path: str
        :param list_obj: stations.validators.ValidatorLog.log
        :return:
        """
        with open(file_path, 'w') as file:
            yaml.safe_dump(log, file, indent=4, default_flow_style=False)

        # with open(file_path, "w", encoding='cp1252') as file:
        #     json.dump(log, file, indent=4)


class ExcelWriter(WriterBase, ABC):
    """
    """
    def __init__(self, *args, **kwargs):
        super(ExcelWriter, self).__init__()
        self.update_attributes(**kwargs)

    def write(self, file_path, data, **kwargs):
        """Write ValidatorLog.log to excel file.

        Args:
            file_path (str): Path to file
            exclude_approved_formats (bool): False | True. If True only disapproved tests will
                                                           be included in the file.
        """
        log_copy = copy.deepcopy(data)

        out_dict = self.get_writer_format(log_copy)
        df = pd.DataFrame(out_dict)

        df.to_excel(
            file_path,
            sheet_name='log',
            na_rep='',
            index=None,
        )

    def get_writer_format(self, data):
        """Return ValidatorLog.log in format likeable to this writer.
        stnreg_import:
            coordinates_dm:
                approved:
                    All good!
                disapproved: {}
        """
        out_dict = {
            'delivery': [],
            'validator': [],
            'disapproved': [],
            'approved': [],
            'comnt': [],
        }
        for delivery, item in data.items():
            for validator_name, item_element in item.items():
                for key_type, item_type in item_element['disapproved'].items():
                    out_dict['delivery'].append(delivery)
                    out_dict['validator'].append(validator_name)
                    out_dict['disapproved'].append(key_type)
                    out_dict['approved'].append(None)
                    out_dict['comnt'].append(item_type)
                for key_type, item_type in item_element['approved'].items():
                    out_dict['delivery'].append(delivery)
                    out_dict['validator'].append(validator_name)
                    out_dict['approved'].append(key_type)
                    out_dict['disapproved'].append(None)
                    out_dict['comnt'].append('Approved')

        return out_dict
