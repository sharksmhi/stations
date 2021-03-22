# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-11-26 17:53

@author: a002028

"""
from stations.main import App


if __name__ == '__main__':
    app = App()

    app.read_list(
        'C:\\station_exports\\uppdateringar\\nya_synonyms.txt',
        reader='shark_master',
        list_name='master'
    )

    app.write_list(
        writer='stnreg',
        list_names='master',
    )