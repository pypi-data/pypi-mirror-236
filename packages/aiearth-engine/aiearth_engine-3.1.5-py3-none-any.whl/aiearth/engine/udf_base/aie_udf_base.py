#!/usr/bin/env python
# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

from aiearth.engine.udf_base.images import ImageSet, Image
from aiearth.engine.udf_base.udf_utils import UDFUtils


class AIEUDF(metaclass=ABCMeta):

    @abstractmethod
    def execute(self, image_set: ImageSet) -> Image:
        pass

    def do_execute(self, images_wrapper) -> bytes:
        image_set = UDFUtils.images_wrapper_to_set(images_wrapper)
        result_image = self.execute(image_set)
        return UDFUtils.image_to_wrapper(result_image).SerializeToString()
