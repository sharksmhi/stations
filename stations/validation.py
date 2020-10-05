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


class Validator:
    """
    """
    def __init__(self, *args, **kwargs):
        super(Validator, self).__init__()

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


if __name__ == '__main__':
    file_path = 'C:/Arbetsmapp/config/sharkweb_shapefiles/Havsomr_SVAR_2016_3c_CP1252.shp'
    pos_val = PositionValidator(file_path=file_path)
    # point = Point(621820, 6785813)
