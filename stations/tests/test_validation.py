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
        reader='shark_master',
        list_name='master'
    )

    # fid = 'C:\\station_exports\\validerade\\Stationsregistret_validering_gävle_validerad.xlsx'
    # fid = 'C:\\station_exports\\nkp\\Stationsregistret_validering.xlsx'
    fid = 'C:\\station_exports\\natvat\\StnReg03_Inmatningsmall.xlsx'

    app.read_list(
        fid,
        reader='stnreg',
        list_name='stnreg_import'
    )

    app.validate_list('stnreg_import')  #, 'master')

    # from stations.validators.validator import ValidatorLog
    # app.write_list(
    #     writer='validation_log',
    #     data=ValidatorLog.log
    # )
    #
    # app.write_list(
    #     writer='shark_master',
    #     list_names=['master', 'stnreg_import'],
    # )
    app.write_list(
        writer='stnreg',
        list_names='stnreg_import',
    )
    # file_path = 'C:/Arbetsmapp/config/sharkweb_shapefiles/Havsomr_SVAR_2016_3c_CP1252.shp'
    # validator = PositionValidator(file_path=file_path)
    # print('shapes read')
    #
    # report = validator.validate(app.lists['master'])
