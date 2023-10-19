# -*- coding: UTF-8 -*-
try:
    def appU(key=None):
        '''
        
        PC界面相关工具
        # pip install -i https://mirrors.aliyun.com/pypi/simple/ PyQt5
        # pip install -i https://mirrors.aliyun.com/pypi/simple/ PyQt5-tools
        # pip install -i https://mirrors.aliyun.com/pypi/simple/ quamash
        
        '''
        from pyuc.py_app.appU import AppU

        o:AppU = AppU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def ui2pyU(key=None):
        '''
        
        PC界面相关工具
        # pip install -i https://mirrors.aliyun.com/pypi/simple/ PyQt5
        # pip install -i https://mirrors.aliyun.com/pypi/simple/ PyQt5-tools
        
        '''
        from pyuc.py_app.ui2pyU import Ui2pyU

        o:Ui2pyU = Ui2pyU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def windowU(key=None):
        '''
        
        PC界面相关工具
        # pip install -i https://mirrors.aliyun.com/pypi/simple/ PyQt5
        # pip install -i https://mirrors.aliyun.com/pypi/simple/ PyQt5-tools
        
        '''
        from pyuc.py_app.windowU import WindowU

        o:WindowU = WindowU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def chromeU(key=None):
        '''
        
        网页浏览器模拟工具
        
        '''
        from pyuc.py_crawl.chromeU import ChromeU

        o:ChromeU = ChromeU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def httpU(key=None):
        '''
        
        接口请求
        
        '''
        from pyuc.py_crawl.httpU import HttpU

        o:HttpU = HttpU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def recordU(key=None):
        '''
        
        ???
        
        '''
        from pyuc.py_crawl.recordU import RecordU

        o:RecordU = RecordU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def scrapyCommandU(key=None):
        '''
        
        scrapy相关命令行操作
        
        '''
        from pyuc.pyuc.py_crawl.scrapyCommandU import ScrapyCommandU

        o:ScrapyCommandU = ScrapyCommandU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def scrapycommandname(key=None):
        '''
        
        '''
        from pyuc.py_crawl.scrapyCommandDemo import Scrapycommandname

        o:Scrapycommandname = Scrapycommandname.produce(key)
        return o
except ImportError as e:
    pass

try:
    def scrapyCommandU(key=None):
        '''
        
        scrapy相关命令行操作
        
        '''
        from pyuc.py_crawl.scrapyCommandU import ScrapyCommandU

        o:ScrapyCommandU = ScrapyCommandU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def scrapyItemU(key=None):
        '''
        
        scrapy相关封装工具的数据存储项基类
        
        '''
        from pyuc.py_crawl.scrapyItemU import ScrapyItemU

        o:ScrapyItemU = ScrapyItemU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def scrapyRunU(key=None):
        '''
        
        ScrapyRun相关封装工具
        
        '''
        from pyuc.py_crawl.scrapyRunU import ScrapyRunU

        o:ScrapyRunU = ScrapyRunU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def scrapySpiderU(key=None):
        '''
        
        scrapy相关封装工具的各个爬虫器
        
        '''
        from pyuc.pyuc.py_crawl.scrapySpiderU import ScrapySpiderU

        o:ScrapySpiderU = ScrapySpiderU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def scrapyItemU(key=None):
        '''
        
        scrapy相关封装工具的数据存储项基类
        
        '''
        from pyuc.pyuc.py_crawl.scrapyItemU import ScrapyItemU

        o:ScrapyItemU = ScrapyItemU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def scrapyspidername(key=None):
        '''
        
        '''
        from pyuc.py_crawl.scrapySpiderDemo import Scrapyspidername

        o:Scrapyspidername = Scrapyspidername.produce(key)
        return o
except ImportError as e:
    pass

try:
    def scrapySpiderU(key=None):
        '''
        
        scrapy相关封装工具的各个爬虫器
        
        '''
        from pyuc.py_crawl.scrapySpiderU import ScrapySpiderU

        o:ScrapySpiderU = ScrapySpiderU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def scrapyU(key=None):
        '''
        
        scrapy相关封装工具
        
        '''
        from pyuc.py_crawl.scrapyU import ScrapyU

        o:ScrapyU = ScrapyU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def webU(key=None):
        '''
        
        网页浏览器模拟工具
        
        '''
        from pyuc.py_crawl.webU import WebU

        o:WebU = WebU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def mongoDBU(key=None):
        '''
        
        Mongo数据库工具
        
        '''
        from pyuc.py_db.mongoDBU import MongoDBU

        o:MongoDBU = MongoDBU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def mysqlDBU(key=None):
        '''
        
        mysql数据库操作工具
        
        '''
        from pyuc.py_db.mysqlDBU import MysqlDBU

        o:MysqlDBU = MysqlDBU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def mysqlU(key=None):
        '''
        
        mysql数据库工具
        
        '''
        from pyuc.py_db.mysqlU import MysqlU

        o:MysqlU = MysqlU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def redisDBU(key=None):
        '''
        
        Redis数据库工具
        
        '''
        from pyuc.py_db.redisDBU import RedisDBU

        o:RedisDBU = RedisDBU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def fileU(key=None):
        '''
        
        文件相关工具
        
        '''
        from pyuc.py_file.fileU import FileU

        o:FileU = FileU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def videoU(key=None):
        '''
        
        视频文件格式相关工具
        
        '''
        from pyuc.py_file.videoU import VideoU

        o:VideoU = VideoU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def algorithmU(key=None):
        '''
        
        算法相关工具
        
        '''
        from pyuc.py_mix.algorithmU import AlgorithmU

        o:AlgorithmU = AlgorithmU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def asyncU(key=None):
        '''
        
        异步相关工具
        
        '''
        from pyuc.py_mix.asyncU import AsyncU

        o:AsyncU = AsyncU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def cmdU(key=None):
        '''
        
        命令行相关工具
        
        '''
        from pyuc.py_mix.cmdU import CmdU

        o:CmdU = CmdU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def ctrlCU(key=None):
        '''
        
        信号相关工具
        
        '''
        from pyuc.py_mix.ctrlCU import CtrlCU

        o:CtrlCU = CtrlCU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def datetimeU(key=None):
        '''
        
        时间日期相关工具 
        
        
        时间格式类型: 
        
        %y 两位数的年份表示（00-99）
        
        %Y 四位数的年份表示（000-9999）
        
        %m 月份（01-12）
        
        %d 月内中的一天（0-31）
        
        %H 24小时制小时数（0-23）
        
        %I 12小时制小时数（01-12）
        
        %M 分钟数（00=59）
        
        %S 秒（00-59）
        
        %a 本地简化星期名称
        
        %A 本地完整星期名称
        
        %b 本地简化的月份名称
        
        %B 本地完整的月份名称
        
        %c 本地相应的日期表示和时间表示
        
        %j 年内的一天（001-366）
        
        %p 本地A.M.或P.M.的等价符
        
        %U 一年中的星期数（00-53）星期天为星期的开始
        
        %w 星期（0-6），星期天为星期的开始
        
        %W 一年中的星期数（00-53）星期一为星期的开始
        
        %x 本地相应的日期表示
        
        %X 本地相应的时间表示
        
        %Z 当前时区的名称
        
        %% %号本身
        
        
        '''
        from pyuc.py_mix.datetimeU import DatetimeU

        o:DatetimeU = DatetimeU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def envU(key=None):
        '''
        
        环境变量相关工具
        
        '''
        from pyuc.py_mix.envU import EnvU

        o:EnvU = EnvU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def jsonU(key=None):
        '''
        
        json
        
        '''
        from pyuc.py_mix.jsonU import JsonU

        o:JsonU = JsonU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def jsU(key=None):
        '''
        
        js工具
        
        '''
        from pyuc.py_mix.jsU import JsU

        o:JsU = JsU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def mathU(key=None):
        '''
        
        数学相关工具
        
        '''
        from pyuc.py_mix.mathU import MathU

        o:MathU = MathU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def moduleU(key=None):
        '''
        
        模块相关工具
        
        '''
        from pyuc.py_mix.moduleU import ModuleU

        o:ModuleU = ModuleU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def objU(key=None):
        '''
        
        obj相关操作工具
        
        '''
        from pyuc.py_mix.objU import ObjU

        o:ObjU = ObjU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def sortU(key=None):
        '''
        
        排序相关工具
        
        '''
        from pyuc.py_mix.sortU import SortU

        o:SortU = SortU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def speechU(key=None):
        '''
        
        语言转化相关工具，文本转语音
        
        '''
        from pyuc.py_mix.speechBaiduU import SpeechU

        o:SpeechU = SpeechU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def speechU(key=None):
        '''
        
        语言转化相关工具，文本转语音
        
        '''
        from pyuc.py_mix.speechU import SpeechU

        o:SpeechU = SpeechU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def threadU(key=None):
        '''
        
        线程相关工具
        
        '''
        from pyuc.py_mix.threadU import ThreadU

        o:ThreadU = ThreadU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def xmlU(key=None):
        '''
        
        XML
        pip install xmltodict
        
        '''
        from pyuc.py_mix.xmlU import XmlU

        o:XmlU = XmlU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def modelU(key=None):
        '''
        
        模型相关工具
        
        '''
        from pyuc.py_pfm.modelU import ModelU

        o:ModelU = ModelU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def pfmU(key=None):
        '''
        
        预测模型相关工具
        
        '''
        from pyuc.py_pfm.pfmU import PfmU

        o:PfmU = PfmU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def adbU(key=None):
        '''
        
        adb相关工具
        
        '''
        from pyuc.py_phone.adbU import AdbU

        o:AdbU = AdbU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def phoneAutoU(key=None):
        '''
        
        手机自动化相关工具
        
        '''
        from pyuc.py_phone.phoneAutoU import PhoneAutoU

        o:PhoneAutoU = PhoneAutoU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def proxyCrawlerU(key=None):
        '''
        
        代理相关工具
        
        '''
        from pyuc.py_proxy.proxyCrawlerU import ProxyCrawlerU

        o:ProxyCrawlerU = ProxyCrawlerU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def proxyInfoU(key=None):
        '''
        
        代理信息相关工具
        
        '''
        from pyuc.py_proxy.proxyInfoU import ProxyInfoU

        o:ProxyInfoU = ProxyInfoU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def proxyU(key=None):
        '''
        
        代理相关工具
        
        '''
        from pyuc.py_proxy.proxyU import ProxyU

        o:ProxyU = ProxyU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def imgU(key=None):
        '''
        
        图片相关工具
        
        '''
        from pyuc.py_recg.imgU import ImgU

        o:ImgU = ImgU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def httpHandlerU(key=None):
        '''
        
        HTTP服务器端接口基类
        
        '''
        from pyuc.py_server.httpHandlerU import HttpHandlerU

        o:HttpHandlerU = HttpHandlerU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def httpServerU(key=None):
        '''
        
        HTTP服务器端相关工具
        
        '''
        from pyuc.py_server.httpServerU import HttpServerU

        o:HttpServerU = HttpServerU.produce(key)
        return o
except ImportError as e:
    pass

try:
    def serverU(key=None):
        '''
        
        服务器端相关工具
        
        '''
        from pyuc.py_server.serverU import ServerU

        o:ServerU = ServerU.produce(key)
        return o
except ImportError as e:
    pass

