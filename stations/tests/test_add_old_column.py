# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-10-21 13:30

@author: a002028

"""
import pandas as pd
import numpy as np


df_old = pd.read_csv(
    'C:/Temp/config/station.txt',
    header=0,
    sep='\t',
    encoding='cp1252',
    dtype=str,
    keep_default_na=False,
)

df_new = pd.read_csv(
    'C:/Arbetsmapp/config/station.txt',
    header=0,
    sep='\t',
    encoding='cp1252',
    dtype=str,
    keep_default_na=False,
)

df_new['EU_CD'] = ''

columns = ['REG_ID', 'REG_ID_GROUP', 'STATION_NAME', 'SYNONYM_NAMES',
       'ICES_STATION_NAME', 'LAT_DM', 'LONG_DM', 'LATITUDE_WGS84_SWEREF99_DD',
       'LONGITUDE_WGS84_SWEREF99_DD', 'LATITUDE_SWEREF99TM',
       'LONGITUDE_SWEREF99TM', 'OUT_OF_BOUNDS_RADIUS', 'WADEP', 'EU_CD', 'MEDIA',
       'COMNT', 'OLD_SHARK_ID']

boolean = df_old['EU_CD'].ne('')

for _, row in df_old.loc[boolean, :].iterrows():
    new_boolean = df_new['STATION_NAME'] == row['STATION_NAME']

    df_new.loc[new_boolean, 'EU_CD'] = row['EU_CD']

# df_new[columns].to_csv(
#             'path_to_new_file.txt',
#             sep='\t',
#             na_rep='',
#             index=False,
#             encoding='cp1252',
#         )