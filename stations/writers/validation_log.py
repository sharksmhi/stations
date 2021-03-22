# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-10-09 17:22

@author: a002028

"""
from abc import ABC

import yaml
# import json
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
