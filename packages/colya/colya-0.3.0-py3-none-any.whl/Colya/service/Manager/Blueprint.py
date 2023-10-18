import re
from flask import Blueprint,render_template,jsonify, request
import json
from Colya.bot import config

def creat_blue_print(callback):
    blue_print = Blueprint("blue_task", __name__)
    data = {
        "consoleLog":[]
    }
    def setValue(key,value):
        data[key] = value
    def getValue(key):
         return data.get(key)
    @blue_print.route('/test',methods=['get'])
    def Test():
        return jsonify({
            'message':'ok',
            'code':0,
        })
    @blue_print.route('/data',methods=['get'])
    def Data():
        return jsonify({
            'message':'ok',
            'code':0,
            "data":data
        })
    @blue_print.route('/cmd',methods=['post'])
    def Cmd():
        data = json.loads(request.data.decode())
        cmds = data.get("cmd")
        cmds = re.sub(r'\s+', ' ', cmds).strip().split(" ")
        if cmds:
            cmd = cmds[0]
            cmds.pop(0)
            args = cmds
            callback(cmd,*args)
        return jsonify({
            'message':'ok',
            'code':0
        })

    return blue_print,setValue,getValue