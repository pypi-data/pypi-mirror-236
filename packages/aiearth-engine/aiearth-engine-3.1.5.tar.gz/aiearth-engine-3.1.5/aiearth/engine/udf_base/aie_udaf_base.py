import json
from abc import ABCMeta, abstractmethod

from aiearth.engine.udf_base.images import Image
from aiearth.engine.udf_base.udf_utils import UDFUtils


class AIEUDAF(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def aggregation(self, image: Image, params) -> None:
        pass

    def agg_wrapper(self, image: Image, params_bytes: bytes, file_path: str, content: str) -> None:
        UDFUtils.save_file(file_path, content)
        self.aggregation(image, json.loads(params_bytes.decode('utf-8')))

    @abstractmethod
    def get_result(self) -> dict:
        pass

    def result_wrapper(self, file_path: str, content: str) -> dict:
        UDFUtils.save_file(file_path, content)
        return self.get_result()
