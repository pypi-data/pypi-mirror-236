# -*- coding: UTF-8 -*-
import pyuc
from pyuc.py_api_b import PyApiB
import base64
import os
if PyApiB.tryImportModule("scrapy", installName="scrapy"):
    from scrapy.http import HtmlResponse


class ScrapyChromeMiddleware(object):
    
    @classmethod
    def process_request(cls, request, spider):
        if spider.crawlType == 'chrome':
            from pyuc.py_crawl.chromeU import ChromeU
            chromeU:ChromeU = pyuc.chromeU().setConfig(isHide=True)
            webdri:str = chromeU.loadUrl(request.url)
            spider.chromeDo(chromeU, request._meta)
            html = chromeU.toHTML()
            chromeU.quit()
            return HtmlResponse(url=request.url,
                                body=html,
                                request=request,
                                encoding='utf-8')
        
        

class ScrapyProxyMiddleware(object):
    
    def getProxyInfo(self):
        proxyHost = pyuc.envU().get('proxy_host','')
        proxyPort = pyuc.envU().get('proxy_port','')
        proxyUser = pyuc.envU().get('proxy_user','')
        proxyPass = pyuc.envU().get('proxy_pswd','')
        if len(proxyHost) == 0:
            return None,None
        proxyServer = None
        if len(proxyHost)>0 and len(proxyPort) > 0:
            proxyServer = f"http://{proxyHost}:{proxyPort}"
        proxyAuth = None
        if len(proxyUser)>0 and len('proxyPass') > 0:
            proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")
        return proxyServer, proxyAuth
    
    def getProxyUInfo(self):
        meta = pyuc.proxyU().getProxyMeta()
        proxy = pyuc.proxyU().metaToProxy(meta)
        if not proxy:
            return None,None
        proxyHost = proxy.get('host','')
        proxyPort = proxy.get('port','')
        proxyUser = proxy.get('user','')
        proxyPass = proxy.get('pswd','')
        if len(proxyHost) == 0:
            return None,None
        proxyServer = None
        if len(proxyHost)>0 and len(proxyPort) > 0:
            proxyServer = f"http://{proxyHost}:{proxyPort}"
        proxyAuth = None
        if len(proxyUser)>0 and len('proxyPass') > 0:
            proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")
        return proxyServer, proxyAuth
    
    def process_request(self, request, spider):
        if request.meta.get('need_proxy', False):
            proxyServer,proxyAuth = self.getProxyUInfo()
            if proxyServer == None:
                proxyServer,proxyAuth = self.getProxyInfo()
            if proxyServer:
                request.meta["proxy"] = proxyServer
            if proxyAuth:
                request.headers["Proxy-Authorization"] = proxyAuth
        
        