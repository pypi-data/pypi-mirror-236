#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from typing import List
import ast

import astunparse as astunparse
from aiearth.core.error import AIEError, AIEErrorCode


class InputParam(object):
    def __init__(self, band_names: List[str]):
        self.input_band_names = band_names

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)


class OutputParam(object):
    def __init__(self, band_names: List[str]):
        self.output_band_names = band_names

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)


def aie_raster_local_udf(input_bands: List[InputParam], output_bands: OutputParam):
    def decorator(cls):
        def wrapper(*args, **kwargs):
            instance = cls(*args, **kwargs)
            return instance

        setattr(wrapper, "udf", "true")
        setattr(wrapper, "clz", cls)
        return wrapper

    return decorator


def aie_raster_zonal_udaf(input_bands: List[InputParam]):
    def decorator(cls):
        def wrapper(*args, **kwargs):
            instance = cls(*args, **kwargs)
            return instance

        setattr(wrapper, "udaf", "true")
        setattr(wrapper, "clz", cls)
        return wrapper

    return decorator


def annotation_parser(source_code):
    module = ast.parse(source_code)
    # 找到使用@aie_raster_local_udf装饰的类
    class_name = None
    target_class = None
    for node in ast.walk(module):
        if isinstance(node, ast.ClassDef):
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Call) and (decorator.func.id == 'aie_raster_local_udf' or decorator.func.id == 'aie_raster_zonal_udaf'):
                    target_class = node
                    break
            if target_class:
                class_name = target_class.name
                break
    if class_name is None or target_class is None:
        raise AIEError(AIEErrorCode.DEFAULT_INTERNAL_ERROR, "注解解析失败，无法获取class_name")

    input_bands = []
    output_bands = []
    for decorator in target_class.decorator_list:
        if isinstance(decorator, ast.Call) and (decorator.func.id == 'aie_raster_local_udf' or decorator.func.id == 'aie_raster_zonal_udaf'):
            for keyword in decorator.keywords:
                if keyword.arg == 'input_bands':
                    for item in eval(astunparse.unparse(keyword.value)):
                        input_bands.append(item.input_band_names)
                elif keyword.arg == 'output_bands':
                    output_bands = eval(astunparse.unparse(keyword.value)).output_band_names

    meta_map = {**InputParam(input_bands).__dict__, **OutputParam(output_bands).__dict__, **{'class_name': class_name}}
    if 'input_band_names' not in meta_map or 'output_band_names' not in meta_map or 'class_name' not in meta_map:
        raise AIEError(AIEErrorCode.DEFAULT_INTERNAL_ERROR, f"注解解析失败，无法获取input_band_names|output_band_names|class_name; meta={json.dumps(meta_map, separators=(',', ':'))}")
    return json.dumps(meta_map, separators=(',', ':'))
