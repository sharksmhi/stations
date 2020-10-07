# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-09-29 18:41

@author: a002028

"""
from abc import ABC

import pandas as pd
import geopandas as gp
from shapely.geometry import Point
from stations.utils import decdeg_to_decmin, transform_ref_system


class Validator:
    """
    """
    def __init__(self, *args, **kwargs):
        super(Validator, self).__init__()
        self.lat_key = None
        self.lon_key = None

    def validate(self, list_obj):
        raise NotImplementedError


class PositionValidator(Validator, ABC):
    """
    """
    def __init__(self, *args, **kwargs):
        super(PositionValidator, self).__init__()
        self.gf = kwargs.get('geodataframe') or gp.read_file(kwargs.get('file_path'))

    def point_in_polygons(self, point):
        """
        With "point_in_polygons" we mean that the point lies in the ocean.
        :param point: shapely.geometry.Point
        :return:
        """
        return self.gf.contains(point).any()

    def validate(self, list_obj):
        """
        :param list_obj:
        :return:
        """
        print('Validating positions..')
        report = {'approved': {},
                  'disapproved': {}}
        for name, north, east in zip(list_obj.get('name'),
                                     list_obj.get('lat_sweref99tm'),
                                     list_obj.get('lon_sweref99tm')):
            point = Point(int(east), int(north))
            validation = self.point_in_polygons(point)
            if validation:
                report['approved'].setdefault(name, (north, east))
            else:
                report['disapproved'].setdefault(name, (north, east))
        print('Validating completed!')
        return report


class Sweref99tmValidator(Validator, ABC):
    """
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


class DegreeValidator(Validator, ABC):
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


class DegreeMinuteValidator(Validator, ABC):
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


if __name__ == '__main__':
    file_path = 'C:/Arbetsmapp/config/sharkweb_shapefiles/Havsomr_SVAR_2016_3c_CP1252.shp'
    pos_val = PositionValidator(file_path=file_path)
    # point = Point(621820, 6785813)
