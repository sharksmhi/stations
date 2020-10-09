# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-09-29 18:41

@author: a002028

"""
import geopandas as gp
from shapely.geometry import Point
from stations.validators.validator import Validator


class PositionValidator(Validator):
    """
    Using SVAR areas to validate if any given position lies in sea water or outside.
    Example of shapefile that can be used: Havsomr_SVAR_2016_3c_CP1252.shp

    NOTE: Version 2016_3c does contain scale errors, new version (may 2021) should be more accurate..
    """
    def __init__(self, *args, **kwargs):
        super(PositionValidator, self).__init__()
        assert ('geodataframe' in kwargs) or ('file_path' in kwargs)
        for key, item in kwargs.items():
            setattr(self, key, item)

        if not hasattr(self, 'geodataframe'):
            self.geodataframe = gp.read_file(kwargs.get('file_path'))

    def point_in_polygons(self, point):
        """
        With "point_in_polygons" we mean that the point lies in the ocean.

        Boolean operation. If any True: return True
        :param point: shapely.geometry.Point
        :return: True / False
        """
        return self.geodataframe.contains(point).any()

    def validate(self, list_obj):
        """
        :param list_obj:
        :return:
        """
        print('Validating positions..')
        report = {'approved': {},
                  'disapproved': {}}
        for name, north, east in zip(list_obj.get('name'),
                                     list_obj.get(self.lat_key),
                                     list_obj.get(self.lon_key)):
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
    point = Point(621820, 6785813)
    print('point_in_polygons:', pos_val.point_in_polygons(point))
