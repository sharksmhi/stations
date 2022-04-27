#!/usr/bin/env python3
# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute.
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-11-30 15:06

@author: johannes
"""
from stations.main import App
from stations import utils
import pandas as pd


if __name__ == '__main__':
    app = App()

    # Read register-template to check delivery stations
    # fid = r'C:\station_exports\lisas_nya\Stationer ifrån SLC-T 2017-2020.xlsx'
    # app.read_list(
    #     fid,
    #     reader='xlsx',
    #     list_name='stnreg_import',
    #     reader_kwargs={'sheet_name': 'Blad1', 'header': 0}
    # )
    fid = r'C:\station_exports\StnReg03_Inmatningsmall.xlsx'
    app.read_list(
        fid,
        reader='xlsx',
        list_name='stnreg_import',
        # reader_kwargs={'sheet_name': 'Blad1', 'header': 0}
    )
    list_obj = app.lists['stnreg_import']

    list_obj.boolean = pd.isnull(list_obj.get('lat_dm'))
    if list_obj.boolean.all():
        list_obj.update_attribute_values('lat_dm',
            [utils.decdeg_to_decmin(p) for p in list_obj.get('lat_dd', boolean=True)]
        )
        list_obj.update_attribute_values('lon_dm',
            [utils.decdeg_to_decmin(p) for p in list_obj.get('lon_dd', boolean=True)]
        )


    list_obj.reset_boolean()
    list_obj.boolean = pd.isnull(list_obj.get('lat_dd'))
    if list_obj.boolean.all():
        list_obj.update_attribute_values('lat_dd',
            [utils.decmin_to_decdeg(p) for p in list_obj.get('lat_dm', boolean=True)]
        )
        list_obj.update_attribute_values('lon_dd',
            [utils.decmin_to_decdeg(p) for p in list_obj.get('lon_dm', boolean=True)]
        )


    list_obj.reset_boolean()
    list_obj.boolean = pd.isnull(list_obj.get('lat_sweref99tm'))
    if list_obj.boolean.all():
        new_lat = []
        new_lon = []
        for la, lo in zip(list_obj.get('lat_dd', boolean=True), list_obj.get('lon_dd', boolean=True)):
            y, x = utils.transform_ref_system(lat=la, lon=lo, out_proj='EPSG:3006', in_proj='EPSG:4326')
            new_lat.append(int(round(y, 0)))
            new_lon.append(int(round(x, 0)))
        list_obj.update_attribute_values('lat_sweref99tm', new_lat)
        list_obj.update_attribute_values('lon_sweref99tm', new_lon)

    app.write_list(
        writer='stnreg',
        list_names='stnreg_import',
    )