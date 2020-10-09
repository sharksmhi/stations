# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-10-01 16:37

@author: a002028

"""
from stations.main import App
from stations.validators.position import PositionValidator

if __name__ == '__main__':
    app = App()
    print('App loaded')
    app.read_list('C:/Arbetsmapp/config/station.txt',
                  header=0,
                  sep='\t',
                  encoding='cp1252',
                  dtype=str,
                  keep_default_na=False,
                  reader='shark_master',
                  list_name='master')
    print('list read')
    file_path = 'C:/Arbetsmapp/config/sharkweb_shapefiles/Havsomr_SVAR_2016_3c_CP1252.shp'
    validator = PositionValidator(file_path=file_path)
    print('shapes read')

    report = validator.validate(app.lists['master'])
