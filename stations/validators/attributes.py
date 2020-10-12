# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-10-12 11:16

@author: a002028

"""
from stations.validators.validator import Validator, ValidatorLog


class MandatoryAttributes(Validator):
    """
    """
    def __init__(self, *args, **kwargs):
        super(MandatoryAttributes, self).__init__()
        for key, item in kwargs.items():
            setattr(self, key, item)

    def validate(self, list_obj):
        """
        :param list_obj: stations.handler.List
        :return:
        """
        assert self.attributes

        report = {'approved': {},
                  'disapproved': {}}

        for attr in self.attributes:
            if list_obj.has_attribute(attr):
                if list_obj.get(attr).all():
                    report['approved'].setdefault(attr, 'No missing values')
                else:
                    report['disapproved'].setdefault(attr, 'WARNING! Missing values')
            else:
                report['disapproved'].setdefault(attr, 'WARNING! Missing attribute')

        ValidatorLog.update_info(
            list_name=list_obj.get('name'),
            validator_name=self.name,
            info=report,
        )
