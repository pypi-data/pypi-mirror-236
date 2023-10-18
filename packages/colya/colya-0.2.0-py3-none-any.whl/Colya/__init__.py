import logging
import json
from logging import handlers
import os

flage = False
if (not os.path.exists('log')):
    os.mkdir('log')
    flage = True

if (not os.path.exists('log/bot.log')):
    open('log/bot.log', "w")
    flage = True


if (not os.path.exists('console.bat')):
    open('console.bat', "w").write(f"node {os.path.join(os.path.dirname(os.path.abspath(__file__)))+'/service/Manager/console/app.js'}")
    flage = True

if (not os.path.exists('console.sh')):
    open('console.sh', "w").write(f"node {os.path.join(os.path.dirname(os.path.abspath(__file__)))+'/service/Manager/console/app.js'}")
    flage = True

if (not os.path.exists('plugin')):
    os.mkdir('plugin')
    flage = True

if (not os.path.exists('config.json')):
    open('config.json', "w").write(json.dumps({
    "host":"127.0.0.1",
    "port":"5500",
    "token":"",
    "heart_beat_cd":10,
    "session_exp_ts":60,
    "console_service":True
    }))
    flage = True
if flage:
    print("目录创建完成，请重启。")
    exit(0)


logger = logging.getLogger()

for h in logger.handlers:
    logger.removeHandler(h)
fmt = "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s"
file_handler = handlers.TimedRotatingFileHandler(
    filename="log/bot.log", encoding='utf-8'
)
file_handler.setFormatter(logging.Formatter(fmt))
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter(fmt))
logger.addHandler(console_handler)
logging.info("Colya启动中。。。")
