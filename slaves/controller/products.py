from flask import Flask, request, jsonify,json
from common import app, sysConfig
from controller import *
import model 

@app.route('/all', methods=['GET']) 
def getDocuments():
    return model.select_all(sysConfig["dbConnConfig"])


@app.route('/title', methods=['GET']) 
def getDocumentByTitle():
    
    type_name = request.args.get('title')
    
    return  model.select_byFilter(sysConfig["dbConnConfig"],type_name)