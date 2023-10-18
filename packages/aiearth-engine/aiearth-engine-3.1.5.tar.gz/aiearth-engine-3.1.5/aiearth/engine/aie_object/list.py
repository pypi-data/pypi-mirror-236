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


class List(FunctionNode):
    def __init__(self, lst: object) -> engine.List:
        if lst is not None and not isinstance(lst, object):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"lst 只支持object类型参数, 传入类型为{type(lst)}"
            )

        invoke_args = {
            "lst": lst,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "lst" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数lst不能为空")

        super(List, self).__init__("List.constructors", invoke_args)

    def add(self, element: object) -> engine.List:
        if element is not None and not isinstance(element, object):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"element 只支持object类型参数, 传入类型为{type(element)}"
            )

        invoke_args = {
            "input": self,
            "element": element,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "element" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数element不能为空")

        return FunctionHelper.apply("List.add", "engine.List", invoke_args)

    def get(self, index: int) -> engine.List:
        if index is not None and not isinstance(index, int):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"index 只支持int类型参数, 传入类型为{type(index)}"
            )

        invoke_args = {
            "input": self,
            "index": index,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "index" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数index不能为空")

        return FunctionHelper.apply("List.get", "engine.List", invoke_args)
