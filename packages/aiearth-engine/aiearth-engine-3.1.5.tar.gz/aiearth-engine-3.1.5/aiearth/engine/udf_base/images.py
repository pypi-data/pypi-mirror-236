#!/usr/bin/env python
# -*- coding: utf-8 -*-
from enum import Enum
from typing import List, Dict


class DataType(Enum):
    UINT8 = 'uint8'
    INT8 = 'int8'
    INT16 = 'int16'
    UINT16 = 'uint16'
    INT32 = 'int32'
    FLOAT32 = 'float32'
    FLOAT64 = 'float64'

    @staticmethod
    def get_type_by_value(value: str):
        for dataType in DataType:
            if dataType.value == value:
                return dataType


class Band(object):
    def __init__(self, data_array, data_type, nodata_value, cols, rows):
        self.data_array = data_array
        self.data_type = data_type
        self.nodata_value = nodata_value
        self.cols = cols
        self.rows = rows


class Image(object):
    def __init__(self, bands: Dict[str, Band]):
        self.bands = bands


class ImageSet(object):
    def __init__(self, images: List[Image], params):
        self.images = images
        self.params = params
