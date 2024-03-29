# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-10-09 12:53

@author: a002028
"""
from stations.validators.validator import Validator, ValidatorLog
from stations.validators.position import PositionInOceanValidator
from stations.validators.coordinates import (
    SweRef99tmValidator,
    DegreeValidator,
    DegreeMinuteValidator
)
from stations.validators.attributes import MandatoryAttributes, MasterAttributes
from stations.validators.identity import Name, Synonyms
