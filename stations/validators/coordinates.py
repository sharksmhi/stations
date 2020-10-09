# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-09-29 18:41

@author: a002028

"""
import pandas as pd
from stations.utils import decdeg_to_decmin, transform_ref_system
from stations.validators.validator import Validator


class Sweref99tmValidator(Validator):
    """
    Coordinates in SWEREF 99TM are mandatory information for any list
    """
    def __init__(self, *args, **kwargs):
        super(Sweref99tmValidator, self).__init__()
        for key, item in kwargs.items():
            setattr(self, key, item)

    def validate(self, list_obj):
        """
        :param list_obj: stations.handler.List
        :return:
        """
        if all(list_obj.get(self.lat_key)) and all(list_obj.get(self.lon_key)):
            return True
        else:
            print('WARNING! we do not have Sweref99tm coordinates for all stations (which is mandatory input)..')
            return False


class DegreeValidator(Validator):
    """
    """
    def __init__(self, *args, **kwargs):
        super(DegreeValidator, self).__init__()
        for key, item in kwargs.items():
            setattr(self, key, item)

    def validate(self, list_obj):
        """
        :param list_obj: stations.handler.List
        :return:
        """
        if not list_obj.has_attribute(self.lat_key):
            d = {self.lat_key: pd.Series([''] * list_obj.length).rename(self.lat_key),
                 self.lon_key: pd.Series([''] * list_obj.length).rename(self.lon_key)}
            list_obj.set_attributes(**d)
        if all(list_obj.get(self.lat_key)) and all(list_obj.get(self.lon_key)):
            return True
        else:
            list_obj.boolean = list_obj.get(self.lat_key).eq('')
            new_lat = []
            new_lon = []
            for lat, lon in zip(list_obj.get('lat_sweref99tm', boolean=True),
                                list_obj.get('lon_sweref99tm', boolean=True)):
                newla, newlo = transform_ref_system(lat=lat, lon=lon)
                new_lat.append(str(round(newla, 6)))
                new_lon.append(str(round(newlo, 6)))
            list_obj.update_attribute_values(self.lat_key, new_lat)
            list_obj.update_attribute_values(self.lon_key, new_lon)


class DegreeMinuteValidator(Validator):
    """
    """
    def __init__(self, *args, **kwargs):
        super(DegreeMinuteValidator, self).__init__()
        for key, item in kwargs.items():
            setattr(self, key, item)

    def validate(self, list_obj):
        """
        :param list_obj: stations.handler.List
        :return:
        """
        if not list_obj.has_attribute(self.lat_key):
            d = {self.lat_key: pd.Series([''] * list_obj.length).rename(self.lat_key),
                 self.lon_key: pd.Series([''] * list_obj.length).rename(self.lon_key)}
            list_obj.set_attributes(**d)
        if all(list_obj.get(self.lat_key)):
            return True
        else:
            list_obj.boolean = list_obj.get(self.lat_key).eq('')
            new_lat = [decdeg_to_decmin(p) for p in list_obj.get('lat_dd', boolean=True)]
            new_lon = [decdeg_to_decmin(p) for p in list_obj.get('lon_dd', boolean=True)]
            list_obj.update_attribute_values(self.lat_key, new_lat)
            list_obj.update_attribute_values(self.lon_key, new_lon)
