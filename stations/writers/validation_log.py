# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-10-09 17:22

@author: a002028

"""
import yaml
from stations.writers.writer import WriterBase


class ValidationWriter(WriterBase):
    """
    """
    def __init__(self, *args, **kwargs):
        super(ValidationWriter, self).__init__()
        for key, item in kwargs.items():
            setattr(self, key, item)

    @staticmethod
    def write(file_path, log):
        """
        :param file_path: str
        :param list_obj: stations.validators.ValidatorLog.log
        :return:
        """
        #TODO use json instead
        with open(file_path, 'w') as file:
            yaml.safe_dump(log, file, indent=4, default_flow_style=False)
