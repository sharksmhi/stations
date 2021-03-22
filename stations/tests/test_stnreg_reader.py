# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-10-05 08:51

@author: a002028

"""
from stations.main import App


if __name__ == '__main__':
    app = App()
    print('App loaded')

    # fid = 'C:\\station_exports\\Stationsregistret_validering_gävle_validerad.xlsx'
    fid = 'C:\\station_exports\\nkp\\StnReg03_Inmatningsmall.xlsx'

    app.read_list(
        fid,
        reader='xlsx',
        list_name='stnreg_import'
    )
    app.validate_list('stnreg_import')
    app.write_list(
        writer='stnreg',
        list_names='stnreg_import',
    )
