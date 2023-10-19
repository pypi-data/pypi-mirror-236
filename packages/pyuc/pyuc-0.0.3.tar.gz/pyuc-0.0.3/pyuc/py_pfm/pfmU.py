# -*- coding: UTF-8 -*-
import pyuc
from pyuc.py_api_b import PyApiB


class PfmU(PyApiB):
    """
    预测模型相关工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def create(self, modelFile):
        from .modelU import ModelU
        c:ModelU = pyuc.modelU()
        c.init(modelFile)
        return c
