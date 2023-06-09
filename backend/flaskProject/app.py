import certifi
import pymongo
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
import json
from waitress import serve

from controllers.productoController import ProductoController

app = Flask(__name__)
cors = CORS(app)
product = ProductoController()


#-----------------RUTAS DE PRODUCTOS-----------------#
@app.route('/productos' , methods=['POST'])
def crearProducto():
    data = request.get_json()
    json = product.create(data)
    return jsonify(json)

@app.route('/productos/<string:id>' , methods=['PUT'])
def actualizarProducto(id):
    data = request.get_json()
    json = product.updateProduct(id,data)
    return jsonify(json)

@app.route('/productos/getAll' , methods=['GET'])
def getAllProducto():
    json = product.getAllProducts()
    return jsonify(json)

@app.route('/productos/getById/<string:id>', methods = ['GET'])
def getById(id):
    json = product.getById(id)
    return jsonify(json)


# -----------CONFIG AND MAIN ROOT-----------#
def loadFileConfig():
    with open('config.json') as f:
        data = json.load(f)
    return data


@app.route('/', methods=['GET'])
def test():
    json = {
        "message": "server is running",
        "port": 5000
    }
    return jsonify(json)




if __name__ == '__main__':
    dataConfig = loadFileConfig()
    print("Server running: " + "http://" + dataConfig["url-backend"] + ":" + str(dataConfig["port"]))
    serve(app, host=dataConfig["url-backend"], port=dataConfig["port"])
