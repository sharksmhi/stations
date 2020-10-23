# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-10-05 14:58

@author: a002028

"""
from stations.main import App
from stations.validators.validator import ValidatorLog


if __name__ == '__main__':
    app = App()

    app.read_list(
        'C:/Arbetsmapp/config/station.txt',
        header=0,
        sep='\t',
        encoding='cp1252',
        dtype=str,
        keep_default_na=False,
        reader='shark_master',
        list_name='master'
    )

    app.read_list(
        'C:/station_exports/validerade/Stationsregistret_validering_gävle_inre.xlsx',
        sheet_name='Provplatser',
        header=0,
        dtype=str,
        keep_default_na=False,
        reader='xlsx',
        list_name='stnreg_import'
    )

    app.validate_list('stnreg_import')

    app.write_list(
        writer='shark_master',
        list_names=['master', 'stnreg_import'],
    )

    app.write_list(
        writer='validation_log',
        data=ValidatorLog.log
    )
