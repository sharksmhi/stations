#!/usr/bin/env python3
# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute.
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-11-30 13:35

@author: johannes
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
    fid = r'C:\station_exports\lisas_nya\Stationer ifrån SLC-T 2017-2020_stnreg_fmt.xlsx'
    app.read_list(
        fid,
        reader='stnreg',
        list_name='lisas_import_2',
    )

    # Validate selected list based on "list_name"
    app.validate_list('lisas_import_2')
    from stations.validators.validator import ValidatorLog
    app.write_list(
        writer='xlsx_validation_log',
        data=ValidatorLog.log
    )

    # # Write master and new list to map
    # app.write_list(writer='map', list_names=['master', 'lisas_import_2'])
