from flask import Flask, request, jsonify,json
from common import app, sysConfig
from controller import *
import model 

@app.route('/', methods=['GET']) 
def main():
    return f"Server {sysConfig['server_name']} running"

@app.route('/documents', methods=['GET']) 
def getDocuments():
    title = request.args.get('title')
    if title == None:
        return model.select_all(sysConfig["dbConnConfig"], sysConfig['db_name'])
    
    return  model.select_byFilter(sysConfig["dbConnConfig"],sysConfig['db_name'], title)