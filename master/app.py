from flask import Flask, request, jsonify, json
import requests

app = Flask(__name__)

SLAVES_IP = "127.0.0.1"
SLAVES_PORT = 4000

SLAVES_DISTR = {
    'tesis': f"{SLAVES_IP}:{SLAVES_PORT}",
    'libro': f"{SLAVES_IP}:{SLAVES_PORT + 1}",
    'video': f"{SLAVES_IP}:{SLAVES_PORT + 2}",
    'presentacion': f"{SLAVES_IP}:{SLAVES_PORT + 3}"
}

@app.route('/')
def hello():
    return 'Server running'


@app.route('/query', methods=['GET']) 
def process_request():
    result = []

    titles = request.args.get('titulo')
    doc_types = request.args.get('tipo_doc') 

    # request a esclavos via tipo de documento
    if doc_types is not None:
        for doc_type in doc_types.split():
            try:
                result += requests.get("http://" + SLAVES_DISTR[doc_type] + "/documents").json()
            except:
                print(f"Request failed - {SLAVES_DISTR[doc_type]}")
        return result
        

    # request a esclavos via titulo
    if titles is not None:
        for slave_distr in SLAVES_DISTR.values():
            try:
                requests.get("http://" + slave_distr + "/documents?title=" + titles.replace(' ', '+')).json()
                result += requests.get("http://" + slave_distr + "/documents?title=" + titles.replace(' ', '+')).json()
            except:
                print(f"Request failed - {slave_distr}")
        return result
    
    
    return "bad request"


app.run(debug=True, port=5000)