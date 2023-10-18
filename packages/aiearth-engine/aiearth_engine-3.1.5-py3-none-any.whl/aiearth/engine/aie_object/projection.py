#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations

import abc
import inspect
from typing import Union
from types import FunctionType

from aiearth import engine
from aiearth.engine.variable_node import VariableNode
from aiearth.engine.function_node import FunctionNode
from aiearth.engine.customfunction_node import CustomFunctionNode
from aiearth.engine.function_helper import FunctionHelper
from aiearth.core.error.aie_error import AIEError, AIEErrorCode


class Projection(FunctionNode):
    def __init__(self, string: str) -> engine.Projection:
        if string is not None and not isinstance(string, str):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"string 只支持str类型参数, 传入类型为{type(string)}"
            )

        invoke_args = {
            "string": string,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "string" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数string不能为空")

        super(Projection, self).__init__("Projection.constructors", invoke_args)

    def crs(self) -> object:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Projection.crs", "object", invoke_args)

    def wkt(self) -> object:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Projection.wkt", "object", invoke_args)

    def proj(self) -> object:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Projection.proj", "object", invoke_args)

    def coordinateTransform(self, src: engine.Projection, xs: list, ys: list) -> object:
        if src is not None and not isinstance(src, engine.Projection):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"src 只支持engine.Projection类型参数, 传入类型为{type(src)}",
            )

        if xs is not None and not isinstance(xs, list):
            raise AIEError(AIEErrorCode.ARGS_ERROR, f"xs 只支持list类型参数, 传入类型为{type(xs)}")

        if ys is not None and not isinstance(ys, list):
            raise AIEError(AIEErrorCode.ARGS_ERROR, f"ys 只支持list类型参数, 传入类型为{type(ys)}")

        invoke_args = {
            "input": self,
            "src": src,
            "xs": xs,
            "ys": ys,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "src" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数src不能为空")

        if "xs" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数xs不能为空")

        if "ys" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数ys不能为空")

        return FunctionHelper.apply(
            "Projection.coordinateTransform", "object", invoke_args
        )
