from flask import Flask, json
import time,sys

###############################################################################
current_milli_time = lambda: int(round(time.time() * 1000))

###############################################################################


def read_config():
    print("#################################################################")
    print("Cantidad de argumentos:{}".format(len(sys.argv)))
    print("Lista de argumentos:{}".format(sys.argv))
    print("#################################################################")


    if len(sys.argv) < 2:
        print("error, debe ingresar el nombre del archivo de configuracion")
        sys.exit(1)

    configFile = sys.argv[1]

    data = ""
    with open(configFile) as json_file:
        data = json.load(json_file)
    return  data
###############################################################################

#CONSTANTE DEL SISTEMA
app = Flask(__name__)
sysConfig = read_config()