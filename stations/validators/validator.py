# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-10-09 12:54

@author: a002028

"""
from abc import ABC


class Validator(ABC):
    """
    Base class for validators.
    """
    def __init__(self, *args, **kwargs):
        super(Validator, self).__init__()
        self.lat_key = None
        self.lon_key = None

    def validate(self, list_obj):
        raise NotImplementedError
