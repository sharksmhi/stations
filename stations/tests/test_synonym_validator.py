#!/usr/bin/env python
# Copyright (c) 2022 SMHI, Swedish Meteorological and Hydrological Institute.
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2022-04-28 11:22

@author: johannes
"""
from stations.main import App
from stations.validators.validator import ValidatorLog


if __name__ == '__main__':
    app = App()

    app.read_list(
        'C:/Arbetsmapp/config/station.txt',
        reader='shark_master',
        list_name='master'
    )
    fid = r'C:\station_exports\mikael_tst\StnReg03_Inmatningsmall_ZB_SLCT.xlsx'

    app.read_list(
        fid,
        reader='stnreg',
        list_name='stnreg_import'
    )

    app.validate_list('stnreg_import', validator_list=['synonyms_in_master'])

    app.write_list(
        writer='xlsx_validation_log',
        data=ValidatorLog.log
    )
