import json
import  logging

class Config:
    def __init__(self) -> None:
        try:
            self.config = json.load(open('config.json','r',encoding='utf-8'))
        except:
            logging.error('获取config.json失败')
            exit(0)
    def getConfig(self,key,default=None):
        return self.config.get(key,default)
    def getPort(self):
        return self.config.get('port','5500')
    def getHost(self):
        return self.config.get('host','localhost')
    def getToken(self):
        token = self.config.get('token',None)
        if not token:
            logging.error('token为空')
            exit(0)
        return token
    def getHeartbeatCd(self):
        return self.config.get('heart_beat_cd',60)