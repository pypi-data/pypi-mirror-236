#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import struct

import filelock
import numpy as np
from aiearth.core.error import AIEError, AIEErrorCode

from aiearth.engine.udf_base import UDFImages_pb2
from aiearth.engine.udf_base.images import DataType, Band, Image, ImageSet


class UDFUtils(object):
    @staticmethod
    def tile_data_decode(dataType: DataType, original_data: bytes) -> np.ndarray:
        def handle_invalid():
            raise AIEError(AIEErrorCode.DEFAULT_INTERNAL_ERROR, "不支持的数据类型=" + dataType.value)

        '''
        np.int8：有符号8位整数类型；
        np.uint8：无符号8位整数类型；
        np.int16：有符号16位整数类型；
        np.uint16：无符号16位整数类型；
        np.int32：有符号32位整数类型；
        np.float32：单精度浮点数类型；
        np.float64：双精度浮点数类型；
        '''
        decode_switcher = {
            DataType.UINT8: lambda: np.frombuffer(original_data, dtype=np.uint8),
            DataType.INT8: lambda: np.frombuffer(original_data, dtype=np.int8),
            DataType.UINT16: lambda: np.frombuffer(original_data, dtype=np.uint16),
            DataType.INT16: lambda: np.frombuffer(original_data, dtype=np.uint16),
            DataType.INT32: lambda: np.frombuffer(original_data, dtype=np.int32),
            DataType.FLOAT32: lambda: np.frombuffer(original_data, dtype=np.float32),
            DataType.FLOAT64: lambda: np.frombuffer(original_data, dtype=np.float64),
        }
        return decode_switcher.get(dataType, handle_invalid)()

    @staticmethod
    def tile_data_encode(dataType: DataType, original_data: np.ndarray) -> bytes:
        def handle_invalid():
            raise AIEError(AIEErrorCode.ARGS_ERROR, "不支持的数据类型=" + dataType.value)

        '''
        'b'：有符号的8位整数类型；
        'B'：无符号的8位整数类型；
        'h'：有符号的16位整数类型；
        'H'：无符号的16位整数类型；
        'i'：有符号的32位整数类型；
        'f'：单精度浮点数类型；
        'd'：双精度浮点数类型；
        '''
        encode_switcher = {
            DataType.UINT8: lambda: struct.pack('<' + 'B' * len(original_data), *original_data),
            DataType.INT8: lambda: struct.pack('<' + 'b' * len(original_data), *original_data),
            DataType.UINT16: lambda: struct.pack('<' + 'H' * len(original_data), *original_data),
            DataType.INT16: lambda: struct.pack('<' + 'h' * len(original_data), *original_data),
            DataType.INT32: lambda: struct.pack('<' + 'i' * len(original_data), *original_data),
            DataType.FLOAT32: lambda: struct.pack('<' + 'f' * len(original_data), *original_data),
            DataType.FLOAT64: lambda: struct.pack('<' + 'd' * len(original_data), *original_data),
        }
        return encode_switcher.get(dataType, handle_invalid)()

    @staticmethod
    def images_wrapper_to_set(imagesWrapper) -> ImageSet:
        images_wrapper = UDFImages_pb2.Wrapper()
        images_wrapper.ParseFromString(imagesWrapper)
        image_list = []
        params = images_wrapper.params
        for img in images_wrapper.image:
            bands = {}
            band_data = img.bandData
            for band_name, band in band_data.items():
                data_type = DataType.get_type_by_value(band.dataType)
                decode_data = UDFUtils.tile_data_decode(data_type, band.tileData)
                nodata_value = band.nodataValue
                cols = band.cols
                rows = band.rows
                bands[band_name] = Band(decode_data, data_type, nodata_value, cols, rows)
            image_list.append(Image(bands))
        return ImageSet(image_list, json.loads(params))

    @staticmethod
    def image_to_wrapper(image: Image) -> UDFImages_pb2.Image:
        image_wrapper = UDFImages_pb2.Image()
        for band_name, band in image.bands.items():
            wrapper_band = UDFImages_pb2.Band()
            wrapper_band.tileData = UDFUtils.tile_data_encode(band.data_type, band.data_array)
            wrapper_band.dataType = band.data_type.value
            wrapper_band.nodataValue = str(band.nodata_value)
            wrapper_band.cols = band.cols
            wrapper_band.rows = band.rows
            image_wrapper.bandData[band_name].CopyFrom(wrapper_band)
        return image_wrapper

    @staticmethod
    def wrapper_to_image(image_bytes: bytes) -> Image:
        image_wrapper = UDFImages_pb2.Image()
        image_wrapper.ParseFromString(image_bytes)
        bands = {}
        band_data = image_wrapper.bandData
        for band_name, band in band_data.items():
            data_type = DataType.get_type_by_value(band.dataType)
            decode_data = UDFUtils.tile_data_decode(data_type, band.tileData)
            nodata_value = band.nodataValue
            cols = band.cols
            rows = band.rows
            bands[band_name] = Band(decode_data, data_type, nodata_value, cols, rows)
        return Image(bands)

    @staticmethod
    def save_file(file_path, content):
        file_name = os.path.basename(file_path)
        lock = filelock.FileLock(file_name + '.lock')
        with lock:
            if not os.path.exists(file_path):
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "w") as file:
                    file.write(content)
