import json
import logging
import asyncio
from Colya.plugin import Loader
from .Session import Session
from Colya.utils import async_call, msgFormat
from .WebSocket import WebSocket
from .Manager import HttpService
from Colya.bot import config as globaConfig

class Work:
    def __init__(self) -> None:
        self.plugin = Loader()
        self.ws =  WebSocket(self.receiveMsg)
        if globaConfig.getConfig("console_service",False):
            self.setHttpService()
        
    def setHttpService(self):
        self.hs = HttpService(self.plugin.matchPluginCmd)
        # 重写日志方法，将日志插入管理面板日志中
        loginfo = logging.info
        def fun(msg, *args, **kwargs):
            msg = str(msg)
            consoleLog = self.hs.getValue('consoleLog')
            consoleLog.append("[INFO]"+msg+''.join(args))
            self.hs.setValue('consoleLog',consoleLog)
            loginfo(msg, *args, **kwargs)
        logging.info = fun
        logwarn = logging.warn
        def fun1(msg, *args, **kwargs):
            msg = str(msg)
            consoleLog = self.hs.getValue('consoleLog')
            consoleLog.append("[Warn]"+msg+''.join(args))
            self.hs.setValue('consoleLog',consoleLog)
            logwarn(msg, *args, **kwargs)
        logging.warn = fun1
        logerror = logging.error
        def fun2(msg, *args, **kwargs):
            msg = str(msg)
            consoleLog = self.hs.getValue('consoleLog')
            consoleLog.append("[ERROR]"+msg+''.join(args))
            self.hs.setValue('consoleLog',consoleLog)
            logerror(msg, *args, **kwargs)
        logging.error = fun2
        def fun3(msg, *args, **kwargs):
            consoleLog = self.hs.getValue('consoleLog')
            consoleLog.append(msg+''.join(args))
            self.hs.setValue('consoleLog',consoleLog)
        logging.text = fun3
        logging.text("输入/help查看帮助")
        
        
    
    def start(self):
        asyncio.get_event_loop().run_until_complete(self.ws.connect())
    

    @async_call
    def receiveMsg(self,msg):
        # data = json.loads(message)
        # 这里直接unescape_special_characters可能会导致混淆
        data = json.loads(msgFormat(msg))
        # print("Dev中信息：", data)
        if data['op'] == 4:
            platform = data['body']['logins'][0]['platform']
            bot_name = data['body']['logins'][0]['user']['name']
            logging.info(f"Satori服务已连接，{bot_name} 已上线 [{platform}] ！")
            self.plugins = self.plugin.load()
            try:
                self.hs.start()
            except:pass
            # Manager.start()
        elif data['op'] == 0:
            session = Session(data["body"])
            user_id = session.user.id
            try:
                self.plugin.matchPlugin(session)
            except Exception as e:
                logging.error("插件运行出错:",e)
            try:
                member = session.user.name
                if not member:
                    member = f'QQ用户{user_id}'
            except:
                # 为什么是QQ用户，因为就QQ可能拿不到成员name...
                member = f'QQ用户{user_id}'
            content = f"['触发事件:'{str(session.type)}][{str(session.guild.name)+'|'+member if session.isGroupMsg else member}]{str(session.message.content)}"
            # logging.info(( {member} )" + session.message.content)
            logging.info(content)
            
        elif data['op'] == 2:
            # print('[心跳状态：存活]')
            # 
            pass