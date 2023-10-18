import asyncio
import json
import websockets
import logging
from Colya.bot import config

class WebSocket:
    def __init__(self,callBack):
        self.token = config.getToken()
        self.ws_url = f"ws://{config.getHost()}:{config.getPort()}/v1/events"
        self.callBack = callBack
    
    async def connect(self):
        # 链接ws
        websocket = await websockets.connect(self.ws_url)
        if(not websocket):
            logging.error("websocket链接失败。。。。。。")
            return None
        logging.info("websocket链接成功,开始连接Satori服务。。。。。。")
        # 链接satori
        await websocket.send(json.dumps({
            "op": 3,
            "body": {
                "token": self.token,
                "sequence": None  # You may set a sequence if needed for session recovery
            }
        }))
        # 心跳测试
        asyncio.create_task(self._heart(websocket))
        # 开始接收消息
        while True:
            try:
                message = await websocket.recv()
                self.callBack(message)
            except websockets.ConnectionClosed:
                logging.error("WebSocket 链接丢失......")
                break
    async def _heart(self,websocket):
        while True:
            await websocket.send(json.dumps({
                "op": 1,
                "body": {
                    "test": "heart"
                }
            }))
            await asyncio.sleep(config.getHeartbeatCd()) 