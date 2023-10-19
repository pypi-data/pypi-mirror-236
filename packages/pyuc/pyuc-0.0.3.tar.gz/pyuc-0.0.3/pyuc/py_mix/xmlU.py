# -*- coding: UTF-8 -*-
import pyuc
from pyuc.py_api_b import PyApiB
import json
if PyApiB.tryImportModule("xmltodict",installName="xmltodict"):
    import xmltodict


class XmlU(PyApiB):
    """
    XML
    pip install xmltodict
    """
    
    
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)
    
    def parseByFile(self, filePath):
        xmlStr = pyuc.fileU().produce().read_str(filePath)
        return self.parseByStr(xmlStr)
    
    def parseByStr(self, xmlStr, **kwargs):
        xmlObj = xmltodict.parse(xmlStr, **kwargs)
        return json.loads(json.dumps(xmlObj))
    