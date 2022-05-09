# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-10-01 16:37

@author: a002028
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

    fid = r'C:\station_exports\mikael_tst\StnReg03_Inmatningsmall_tumlare_all.xlsx'

    app.read_list(
        fid,
        reader='stnreg',
        list_name='tumlare_all'
    )

    app.validate_list('tumlare_all')

    app.write_list(
        writer='xlsx_validation_log',
        data=ValidatorLog.log,
        styled=True
    )

    # app.write_list(
    #     writer='map',
    #     list_names=['master', 'tumlare_all'],
    # )
    # app.write_list(
    #     writer='stnreg',
    #     list_names='tumlare_all',
    # )
    # file_path = 'C:/Arbetsmapp/config/sharkweb_shapefiles/Havsomr_SVAR_2016_3c_CP1252.shp'
    # validator = PositionValidator(file_path=file_path)
    # print('shapes read')
    #
    # report = validator.validate(app.lists['master'])
