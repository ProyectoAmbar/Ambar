from repositories.interfaceRepositorio import interfaceRepositorio
from models.FormatoAlquiler import formatoAlquiler
from bson.objectid import ObjectId
from datetime import date


class repositorioFormatoAlquiler(interfaceRepositorio[formatoAlquiler]):
    def save(self, formAlquiler):
        print("def save")
        collection = self.db[self.collection]
        inserted = collection.insert_one(formAlquiler.__dict__)
        id = inserted.inserted_id.__str__()
        print(id)
        response = collection.find_one({"_id": ObjectId(id)})
        print(response)
        response['_id'] = str(response['_id'])
        response['asesor'] = str(response['asesor'])
        response['Producto'] = str(response['Producto'])

        return response

    def getAll(self):
        allItems = []
        collection = self.db[self.collection]
        response = collection.find()
        for i in response:
            i['_id'] = str(i['_id'])
            i['asesor'] = str(i['asesor'])
            i['Producto'] = str(i['Producto'])
            allItems.append(i)
        return allItems

    def getById(self, id):
        try:
            collection = self.db[self.collection]
            response = collection.find_one({"_id": ObjectId(id)})
            response['_id'] = str(response['_id'])
            response['asesor'] = str(response['asesor'])
            response['Producto'] = str(response['Producto'])

            return response
        except:
            return {"status": False , "code": 400, "message": "no se encontro el id " + id}

    def update(self, id, infoUpdate):
            collection = self.db[self.collection]
            infoUpdate = infoUpdate.__dict__
            print(id)
            collection.update_one({"_id": ObjectId(id)}, {"$set": infoUpdate})
            response = collection.find_one({"_id": ObjectId(id)})
            response['_id'] = str(response['_id'])
            response['asesor'] = str(response['asesor'])
            response['Producto'] = str(response['Producto'])
            return response

    def getByIdToUpdate(self, id):
            collection = self.db[self.collection]
            response = collection.find_one({"_id": ObjectId(id)})
            return response


    def delete(self, id):
        dict = [{
            "status": True,
            "code": 202
        }]
        collection = self.db[self.collection]
        delObject = collection.delete_one({'_id': ObjectId(id)}).deleted_count
        dict.append({"deleted_count": delObject})
        return dict

    def query(self, theQuery):
        laColeccion = self.baseDatos[self.coleccion]
        data = []
        for x in laColeccion.find(theQuery):
            x["_id"] = x["_id"].__str__()
            x['asesor'] = str(x['asesor'])
            x['Producto'] = str(x['Producto'])
        x = self.transformObjectIds(x)
        x = self.getValuesDBRef(x)
        data.append(x)
        return data

    def getEntregaDeProductos(self):
        collection = self.db[self.collection]
        allItems = []
        query = {"fechaDeEntrega": {"$gte": str(date.today())}}
        response = collection.find(query).sort("fechaDeEntrega",1)
        for item in response:
            task = {
                "formulario": str(item['_id']),
                "Producto": str(item['Producto']),
                "asesor": str(item['asesor']),
                "identificacionCliente": item['identificacion'],
                "fechaDeEntrega": item['fechaDeEntrega']
            }
            allItems.append(task)
        return allItems

    def getByFactura(self,Factura):
        try:
            collection = self.db[self.collection]
            response = collection.find_one({'numeroFactura': Factura})
            response['_id'] = str(response['_id'])
            response['asesor'] = str(response['asesor'])
            response['Producto'] = str(response['Producto'])

            return response
        except:
            return {"status": False , "code": 400, "message": "no se encontro el form de factura numero" + Factura}



    pass