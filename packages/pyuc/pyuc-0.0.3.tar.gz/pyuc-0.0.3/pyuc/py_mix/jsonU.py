# -*- coding: UTF-8 -*-
import pyuc
from pyuc.py_api_b import PyApiB
import json


class JsonU(PyApiB):
    """
    json
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def fromString(self, string):
        return json.loads(string)

    def toString(self, json_data, ensure_ascii=False, indent=2):
        return json.dumps(json_data, ensure_ascii=ensure_ascii, indent=indent)

    def fromFile(self, filePath):
        return pyuc.fileU("JsonU").read_json(filePath)

    def toFile(self, json_data, filePath):
        return pyuc.fileU("JsonU").write_json(filePath, json_data)

