# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-10-01 16:37

@author: a002028

"""
from stations.main import App


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

    fid = 'C:\\station_exports\\Stationsregistret_validering_gävle_validerad.xlsx'

    app.read_list(
        fid,
        sheet_name='Provplatser',
        header=0,
        dtype=str,
        keep_default_na=False,
        reader='xlsx',
        list_name='stnreg_import'
    )

    app.validate_list('stnreg_import', 'master')
    from stations.validators.validator import ValidatorLog
    app.write_list(
        writer='validation_log',
        data=ValidatorLog.log
    )
    # file_path = 'C:/Arbetsmapp/config/sharkweb_shapefiles/Havsomr_SVAR_2016_3c_CP1252.shp'
    # validator = PositionValidator(file_path=file_path)
    # print('shapes read')
    #
    # report = validator.validate(app.lists['master'])
