from flask import Flask, request, jsonify,json

app = Flask(__name__)
app.run(debug=True)

@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/products', methods=['GET']) 
def getProducts():

    pname = request.args.get('pname')
    price = request.args.get('price')

    if pname == None and price == None:
        return "list all products" 
    
    return "list products by args => pname={} - price={}".format(pname,price)


@app.route('/products/<id>', methods=['GET']) 
def getProductById(id):
    return "id="+id

@app.route('/products', methods=['POST']) 
def createProduct():
    data = request.json
    print(data)
    #respuesta tipo json jsonify(data)
    return "json enviado => "+ json.dumps(data)

@app.route('/products/<id>', methods=['PUT']) 
def updateProductById(id):
    data = request.json
    #respuesta tipo json jsonify(data)
    return "id => "+id+" - json enviado => "+ json.dumps(data)

@app.route('/products', methods=['DELETE']) 
def deleteProducts():
    return "deleteProducts (no borrar realmente - solo marcar el estado 'eliminado')"

@app.route('/products/<id>', methods=['DELETE']) 
def deleteProductById(id):
    return " id = "+id+" (no borrar realmente - solo marcar el estado 'eliminado')"