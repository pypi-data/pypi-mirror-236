# -*- coding: UTF-8 -*-
from pyuc.py_api_b import PyApiB
from .httpServerU import HttpServerU


class ServerU(PyApiB):
    """
    服务器端相关工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def http(self, port=80) -> HttpServerU:
        return HttpServerU(port)