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


class Number(FunctionNode):
    def __init__(self, number: object) -> engine.Number:
        if number is not None and not isinstance(number, object):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR, f"number 只支持object类型参数, 传入类型为{type(number)}"
            )

        invoke_args = {
            "number": number,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "number" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数number不能为空")

        super(Number, self).__init__("Number.constructors", invoke_args)

    def abs(self) -> engine.Number:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Number.abs", "engine.Number", invoke_args)

    def acos(self) -> engine.Number:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Number.acos", "engine.Number", invoke_args)

    def asin(self) -> engine.Number:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Number.asin", "engine.Number", invoke_args)

    def atan(self) -> engine.Number:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Number.atan", "engine.Number", invoke_args)

    def cbrt(self) -> engine.Number:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Number.cbrt", "engine.Number", invoke_args)

    def ceil(self) -> engine.Number:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Number.ceil", "engine.Number", invoke_args)

    def cos(self) -> engine.Number:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Number.cos", "engine.Number", invoke_args)

    def cosh(self) -> engine.Number:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Number.cosh", "engine.Number", invoke_args)

    def exp(self) -> engine.Number:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Number.exp", "engine.Number", invoke_args)

    def floor(self) -> engine.Number:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Number.floor", "engine.Number", invoke_args)

    def log(self) -> engine.Number:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Number.log", "engine.Number", invoke_args)

    def log10(self) -> engine.Number:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Number.log10", "engine.Number", invoke_args)

    def round(self) -> engine.Number:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Number.round", "engine.Number", invoke_args)

    def signum(self) -> engine.Number:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Number.signum", "engine.Number", invoke_args)

    def sin(self) -> engine.Number:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Number.sin", "engine.Number", invoke_args)

    def sinh(self) -> engine.Number:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Number.sinh", "engine.Number", invoke_args)

    def sqrt(self) -> engine.Number:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Number.sqrt", "engine.Number", invoke_args)

    def tan(self) -> engine.Number:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Number.tan", "engine.Number", invoke_args)

    def tanh(self) -> engine.Number:
        invoke_args = {
            "input": self,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        return FunctionHelper.apply("Number.tanh", "engine.Number", invoke_args)

    def eq(self, right: Union[engine.Number, int, int, float]) -> engine.Number:
        if right is not None and not isinstance(
            right, (engine.Number, int, int, float)
        ):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"right 只支持(engine.Number,int,int,float)类型参数, 传入类型为{type(right)}",
            )

        invoke_args = {
            "input": self,
            "right": right,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "right" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数right不能为空")

        return FunctionHelper.apply("Number.eq", "engine.Number", invoke_args)

    def lt(self, right: Union[engine.Number, int, int, float]) -> engine.Number:
        if right is not None and not isinstance(
            right, (engine.Number, int, int, float)
        ):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"right 只支持(engine.Number,int,int,float)类型参数, 传入类型为{type(right)}",
            )

        invoke_args = {
            "input": self,
            "right": right,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "right" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数right不能为空")

        return FunctionHelper.apply("Number.lt", "engine.Number", invoke_args)

    def lte(self, right: Union[engine.Number, int, int, float]) -> engine.Number:
        if right is not None and not isinstance(
            right, (engine.Number, int, int, float)
        ):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"right 只支持(engine.Number,int,int,float)类型参数, 传入类型为{type(right)}",
            )

        invoke_args = {
            "input": self,
            "right": right,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "right" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数right不能为空")

        return FunctionHelper.apply("Number.lte", "engine.Number", invoke_args)

    def gt(self, right: Union[engine.Number, int, int, float]) -> engine.Number:
        if right is not None and not isinstance(
            right, (engine.Number, int, int, float)
        ):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"right 只支持(engine.Number,int,int,float)类型参数, 传入类型为{type(right)}",
            )

        invoke_args = {
            "input": self,
            "right": right,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "right" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数right不能为空")

        return FunctionHelper.apply("Number.gt", "engine.Number", invoke_args)

    def gte(self, right: Union[engine.Number, int, int, float]) -> engine.Number:
        if right is not None and not isinstance(
            right, (engine.Number, int, int, float)
        ):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"right 只支持(engine.Number,int,int,float)类型参数, 传入类型为{type(right)}",
            )

        invoke_args = {
            "input": self,
            "right": right,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "right" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数right不能为空")

        return FunctionHelper.apply("Number.gte", "engine.Number", invoke_args)

    def neq(self, right: Union[engine.Number, int, int, float]) -> engine.Number:
        if right is not None and not isinstance(
            right, (engine.Number, int, int, float)
        ):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"right 只支持(engine.Number,int,int,float)类型参数, 传入类型为{type(right)}",
            )

        invoke_args = {
            "input": self,
            "right": right,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "right" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数right不能为空")

        return FunctionHelper.apply("Number.neq", "engine.Number", invoke_args)

    def atan2(self, right: Union[engine.Number, int, int, float]) -> engine.Number:
        if right is not None and not isinstance(
            right, (engine.Number, int, int, float)
        ):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"right 只支持(engine.Number,int,int,float)类型参数, 传入类型为{type(right)}",
            )

        invoke_args = {
            "input": self,
            "right": right,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "right" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数right不能为空")

        return FunctionHelper.apply("Number.atan2", "engine.Number", invoke_args)

    def hypot(self, right: Union[engine.Number, int, int, float]) -> engine.Number:
        if right is not None and not isinstance(
            right, (engine.Number, int, int, float)
        ):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"right 只支持(engine.Number,int,int,float)类型参数, 传入类型为{type(right)}",
            )

        invoke_args = {
            "input": self,
            "right": right,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "right" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数right不能为空")

        return FunctionHelper.apply("Number.hypot", "engine.Number", invoke_args)

    def max(self, right: Union[engine.Number, int, int, float]) -> engine.Number:
        if right is not None and not isinstance(
            right, (engine.Number, int, int, float)
        ):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"right 只支持(engine.Number,int,int,float)类型参数, 传入类型为{type(right)}",
            )

        invoke_args = {
            "input": self,
            "right": right,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "right" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数right不能为空")

        return FunctionHelper.apply("Number.max", "engine.Number", invoke_args)

    def min(self, right: Union[engine.Number, int, int, float]) -> engine.Number:
        if right is not None and not isinstance(
            right, (engine.Number, int, int, float)
        ):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"right 只支持(engine.Number,int,int,float)类型参数, 传入类型为{type(right)}",
            )

        invoke_args = {
            "input": self,
            "right": right,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "right" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数right不能为空")

        return FunctionHelper.apply("Number.min", "engine.Number", invoke_args)

    def multiply(self, right: Union[engine.Number, int, int, float]) -> engine.Number:
        if right is not None and not isinstance(
            right, (engine.Number, int, int, float)
        ):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"right 只支持(engine.Number,int,int,float)类型参数, 传入类型为{type(right)}",
            )

        invoke_args = {
            "input": self,
            "right": right,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "right" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数right不能为空")

        return FunctionHelper.apply("Number.multiply", "engine.Number", invoke_args)

    def pow(self, right: Union[engine.Number, int, int, float]) -> engine.Number:
        if right is not None and not isinstance(
            right, (engine.Number, int, int, float)
        ):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"right 只支持(engine.Number,int,int,float)类型参数, 传入类型为{type(right)}",
            )

        invoke_args = {
            "input": self,
            "right": right,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "right" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数right不能为空")

        return FunctionHelper.apply("Number.pow", "engine.Number", invoke_args)

    def add(self, right: Union[engine.Number, int, int, float]) -> engine.Number:
        if right is not None and not isinstance(
            right, (engine.Number, int, int, float)
        ):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"right 只支持(engine.Number,int,int,float)类型参数, 传入类型为{type(right)}",
            )

        invoke_args = {
            "input": self,
            "right": right,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "right" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数right不能为空")

        return FunctionHelper.apply("Number.add", "engine.Number", invoke_args)

    def subtract(self, right: Union[engine.Number, int, int, float]) -> engine.Number:
        if right is not None and not isinstance(
            right, (engine.Number, int, int, float)
        ):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"right 只支持(engine.Number,int,int,float)类型参数, 传入类型为{type(right)}",
            )

        invoke_args = {
            "input": self,
            "right": right,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "right" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数right不能为空")

        return FunctionHelper.apply("Number.subtract", "engine.Number", invoke_args)

    def divide(self, right: Union[engine.Number, int, int, float]) -> engine.Number:
        if right is not None and not isinstance(
            right, (engine.Number, int, int, float)
        ):
            raise AIEError(
                AIEErrorCode.ARGS_ERROR,
                f"right 只支持(engine.Number,int,int,float)类型参数, 传入类型为{type(right)}",
            )

        invoke_args = {
            "input": self,
            "right": right,
        }

        invoke_args = {k: v for k, v in invoke_args.items() if v is not None}

        if "right" not in invoke_args:
            raise AIEError(AIEErrorCode.ARGS_ERROR, "参数right不能为空")

        return FunctionHelper.apply("Number.divide", "engine.Number", invoke_args)
