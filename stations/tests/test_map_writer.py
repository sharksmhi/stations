# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-11-10 11:01

@author: a002028

"""
from stations.main import App


if __name__ == '__main__':
    app = App()

    # Read master list
    app.read_list(
        'C:/Arbetsmapp/config/station.txt',
        reader='shark_master',
        list_name='master'
    )

    # Read register-template to check delivery stations
    #fid = r'C:\Utveckling\TESTING\fb_btl_join\punkter.xlsx'
    # fid = r"C:\mw\dv\StnReg03_Inmatningsmall.xlsx"
    # app.read_list(
    #     fid,
    #     reader='stnreg',
    #     list_name='stnreg_import'
    # )

    fid = r"C:\mw\dv\StnReg03_Inmatningsmall.xlsx"
    app.read_list(
        fid,
        reader='stnreg',
        list_name='test'
    )



    # Validate selected list based on "list_name"
    # app.validate_list('stnreg_import')

    # Write master and new list to map
    app.write_list(
        writer='map',
        # list_names=['master'],
        # list_names=['stnreg_import'],
        # list_names=['master', 'stnreg_import'],
        list_names=['master', 'test'],
        new_stations_as_cluster=False,
    )
