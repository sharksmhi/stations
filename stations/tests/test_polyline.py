# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-10-02 08:56

@author: a002028

"""
from stations.utils import transform_ref_system
from stations.writers.map import MapWriter
from stations.validators.position import PositionValidator


if __name__ == '__main__':
    m = MapWriter(map_settings={'location': [61.75, 19.45],
                                'zoom_start': 5},
                  marker_tag_attributes={'name': 'name',
                                         'id': 'id',
                                         'lat_dd': 'lat_dd',
                                         'lon_dd': 'lon_dd'}
                  )

    file_path = 'C:/Arbetsmapp/config/sharkweb_shapefiles/Havsomr_SVAR_2016_3c_CP1252.shp'
    pos_val = PositionValidator(file_path=file_path)
    # point = Point(621820, 6785813)
    boolean = pos_val.gf['OBJECTID'] == 593

    import numpy as np
    import shapely

    all_coords = []
    for i in pos_val.gf.index:
        print(i)
        boolean = pos_val.gf.index == i
        g = [i for i in pos_val.gf[boolean].geometry]
        if type(g[0].boundary) == shapely.geometry.linestring.LineString:
            coords = np.dstack(g[0].boundary.coords.xy).tolist()
            transformed_points = []
            for p in coords[0]:
                la, lo = transform_ref_system(lon=p[0], lat=p[1])
                transformed_points.append(tuple((la, lo)))

            all_coords.append(*[transformed_points])
        else:
            for b in g[0].boundary:  # for first feature/row
                coords = np.dstack(b.coords.xy).tolist()
                transformed_points = []
                for p in coords[0]:
                    la, lo = transform_ref_system(lon=p[0], lat=p[1])
                    # p = Point(lo, la)
                    transformed_points.append(tuple((la, lo)))

                all_coords.append(*[transformed_points])

    for i, p_list in enumerate(all_coords):
        m.add_polyline(p_list, str(i))

    m._write('map.html')
