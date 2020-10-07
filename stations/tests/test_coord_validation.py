# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-10-06 16:58

@author: a002028

"""
from stations.main import App
from stations.validation import DegreeValidator


if __name__ == '__main__':
    app = App()
    print('App loaded')

    fid = 'C:\\station_exports\\Stationsregistret_validering_gävle_validerad.xlsx'

    app.read_list(fid,
                  sheet_name='Provplatser',
                  header=0,
                  dtype=str,
                  keep_default_na=False,
                  reader='xlsx',
                  list_name='stnreg_import')

    validator = DegreeValidator(lat_key='lat_dd',
                                lon_key='lon_dd')

    validator.validate(app.lists['stnreg_import'])