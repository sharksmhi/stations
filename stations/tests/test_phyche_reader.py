# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-03-20 14:31
@author: johannes
"""
import os
from stations.main import App


if __name__ == '__main__':
    app = App()
    print('App loaded')

    wd = 'C:\\Temp\\DV\\stations_test'
    file_names = (os.path.join(wd, f) for f in os.listdir(wd))
    list_names_to_validate = []
    for i, fid in enumerate(file_names):
        name = 'phyche_import_{}'.format(i+1)
        app.read_list(
            fid,
            reader='phyche',
            list_name=name
        )
        list_names_to_validate.append(name)

    app.read_list(
        'C:/Arbetsmapp/config/station.txt',
        reader='shark_master',
        list_name='master'
    )

    app.validate_list(*list_names_to_validate)

    app.write_list(
        writer='map',
        list_names=['master', *list_names_to_validate],
        station_radius=False,
    )
