# -*- coding: UTF-8 -*-
import pyuc
from pyuc.py_api_b import PyApiB
import random
import string
from .chromeU import ChromeU
from .scrapyItemU import ScrapyItemU
from .scrapySaveItem import ScrapySaveItem
if PyApiB.tryImportModule("scrapy", installName="scrapy"):
    import scrapy
    from scrapy.loader.processors import Identity, MapCompose
    from scrapy.loader import ItemLoader
    from scrapy.loader.processors import TakeFirst


class ScrapySpiderU(scrapy.Spider, PyApiB):
    """
    scrapy相关封装工具的各个爬虫器
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    enable = True
    """
    如果为enable=True,开启这项的spider才会执行
    """
    name = 'SpiderU_default'

    crawlType = 'scrapy'
    """ scrapy默认, chrome：表示启用chrome打开,页面加载完成后，会触发chromeDo进行操作 """

    def chromeDo(self, chromeU: ChromeU, meta=None):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        import random
        import string
        setattr(self,'saveSign',''.join(random.sample(string.ascii_letters + string.digits, 32)))
        self.state = 'waitting'

    def toJsonStr(self, data):
        return pyuc.jsonU().toString(data, indent=None)
    
    def toJson(self, jsonStr):
        return pyuc.jsonU().fromString(jsonStr)
    
    def meta(self, response, key):
        return response.meta[key]

    def get(self, url, callback, meta=None, method='GET', headers=None, body=None,
                 cookies=None, encoding='utf-8', priority=0,
                 dont_filter=False, errback=None, flags=None, cb_kwargs=None):
        return scrapy.Request(url=url, callback=callback, meta=meta, method=method, headers=headers, body=body,
                 cookies=cookies, encoding=encoding, priority=priority,
                 dont_filter=dont_filter, errback=errback, flags=flags, cb_kwargs=cb_kwargs)

    def saveItem(self, data, item_cls: ScrapyItemU):
        """
        yield self.saveItem(data, xxxxItem)
        """
        
        item_loader = ItemLoader(item=item_cls())
        item_loader.default_output_processor = TakeFirst()
        for key in data:
            try:
                item_loader.add_value(key, data[key])
            except BaseException as identifier:
                pass
        return item_loader.load_item()
    
    def saveBegin(self):
        
        setattr(self,'saveSign',''.join(random.sample(string.ascii_letters + string.digits, 32)))
        item_loader = ItemLoader(item=ScrapySaveItem())
        item_loader.default_output_processor = TakeFirst()
        item_loader.add_value('type','begin')
        item_loader.add_value('saveSign',getattr(self,'saveSign'))
        return item_loader.load_item()
    
    def saveCommit(self,optionType='insert'):
        """ option=insert|upsert|jsonfile@filePath """
        item_loader = ItemLoader(item=ScrapySaveItem())
        item_loader.default_output_processor = TakeFirst()
        item_loader.add_value('type','commit')
        item_loader.add_value('saveSign',getattr(self,'saveSign'))
        item_loader.add_value('optionType',optionType)
        return item_loader.load_item()
    
