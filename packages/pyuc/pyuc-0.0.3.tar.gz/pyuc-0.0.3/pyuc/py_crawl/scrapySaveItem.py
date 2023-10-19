import pyuc
from pyuc.py_api_b import PyApiB
if PyApiB.tryImportModule("scrapy",installName="scrapy"):
    import scrapy


class ScrapySaveItem(scrapy.Item):
    """"""
    type = scrapy.Field()
    """"""
    saveSign = scrapy.Field()
    """"""
    optionType = scrapy.Field()
