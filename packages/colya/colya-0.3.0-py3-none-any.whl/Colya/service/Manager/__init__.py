import os
from flask import Flask
from flask_cors import *
from .Blueprint import creat_blue_print
import waitress
import logging
from gevent import pywsgi

class HttpService:
    def __init__(self,callback) -> None:
        # static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Colya/service/Manager/templates/static')
        # template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Colya/service/Manager/templates')
        self.api = Flask(__name__) 
        
        CORS(self.api, supports_credentials=True, resources=r"/*")
        blur_print,self.setValue,self.getValue = creat_blue_print(callback)
        self.api.register_blueprint(blur_print)

    def start(self):
        waitress.serve(self.api, host='127.0.0.1', port="7796")
        # self.api.run(host='127.0.0.1', port=config.getConfig("http_port","7796"))
        # server = pywsgi.WSGIServer(('127.0.0.1', config.getConfig("http_port","7796")), self.api)
        # server.serve_forever()