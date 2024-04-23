from flask import Flask, request, jsonify,json
from common import app, sysConfig
from controller import *
import model 

@app.route('/products', methods=['GET']) 
def getProducts():

    pname = request.args.get('pname')
    price = request.args.get('price')

    if pname == None and price == None:
        return model.select_all(sysConfig["dbConnConfig"])
    
    return model.select_byFilter(sysConfig["dbConnConfig"],pname,price)


@app.route('/products/<int:id>', methods=['GET']) 
def getProductById(id):
    return  model.select_byId(sysConfig["dbConnConfig"],id)

@app.route('/products', methods=['POST']) 
def createProduct():
    data = request.json
    return model.insert(sysConfig["dbConnConfig"],sysConfig["server_name"],sysConfig["subscriber_name"],data)

@app.route('/products/<int:id>', methods=['PUT']) 
def updateProductById(id):
    data = request.json
    return model.update(sysConfig["dbConnConfig"],id,data)

@app.route('/products', methods=['DELETE']) 
def deleteProducts():
    return model.delete_all(sysConfig["dbConnConfig"])

@app.route('/products/<int:id>', methods=['DELETE']) 
def deleteProductById(id):
    return model.delete_byId(sysConfig["dbConnConfig"],id)
