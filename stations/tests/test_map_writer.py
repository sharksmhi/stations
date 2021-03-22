# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-11-10 11:01

@author: a002028

"""
import time
from stations.main import App


if __name__ == '__main__':
    app = App()

    app.read_list(
        'C:/Arbetsmapp/config/station.txt',
        reader='shark_master',
        list_name='master'
    )

    # fid = 'C:\\station_exports\\HAL_PAG\\StnReg03_Inmatningsmall_201215.xlsx'
    # fid = 'C:\\Temp\\DV\\hist_data\\StnReg03_Inmatningsmall.xlsx'
    fid = 'C:\\station_exports\\PELA_Hogakusten\\StnReg_PELA_Hogakusten.xlsx'

    app.read_list(
        fid,
        reader='xlsx',
        list_name='stnreg_import'
    )

    app.validate_list('stnreg_import')

    app.write_list(writer='map', list_names=['master', 'stnreg_import'])

    # start_time = time.time()
    # print(("{} sec".format(time.time() - start_time)))
