# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-10-02 12:18

@author: a002028

"""
from stations.main import App

if __name__ == '__main__':
    app = App()

    new_stations = {'name': ['Hästholmen Syd', 'Svartskär Ost'],
                    'lat_sweref99tm': ['6360582', '6363345'],
                    'lon_sweref99tm': ['317200', '310970'],
                    'lat_dd': [],
                    'lon_dd': []}
    from stations.utils import transform_ref_system

    for la, lo in zip(new_stations['lat_sweref99tm'], new_stations['lon_sweref99tm']):
        lat_dd, lon_dd = transform_ref_system(lat=la, lon=lo)
        new_stations['lat_dd'].append(round(lat_dd, 8))
        new_stations['lon_dd'].append(round(lon_dd, 8))

    app.lists.append_new_list(name='new_stations',
                              data=new_stations,
                              attributes={k: k for k in list(new_stations)}
                              )

    # app.write_list(writer='map', list_names=['new_stations'])
