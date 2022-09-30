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
        reader='shark_master',
        list_name='master'
    )

    app.read_list(
        r'C:\station_exports\natvat\StnReg20Verifiering.xlsx',
        reader='stnreg',
        list_name='stnreg_import'
    )

    app.validate_list('stnreg_import')

    app.write_list(
        writer='shark_master',
        list_names=['master', 'stnreg_import'],
    )
