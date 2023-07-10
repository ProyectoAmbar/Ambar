from repositories.interfaceRepositorio import interfaceRepositorio
from models.FormatoAlquiler import formatoAlquiler
from bson.objectid import ObjectId


class repositorioFormatoAlquiler(interfaceRepositorio[formatoAlquiler]):
    def save(self, formAlquiler):
        dict = []
        print("def save")
        collection = self.db['formatoAlquiler']
        inserted = collection.insert_one(formAlquiler.__dict__)
        id = inserted.inserted_id.__str__()
        print(id)
        response = collection.find_one({"_id": ObjectId(id)})
        print(response)
        response['_id'] = str(response['_id'])
        response['asesor'] = str(response['asesor'])
        response['Producto'] = str(response['Producto'])
        response['Cliente'] = str(response['Cliente'])
        dict.append(response)
        return dict

    def getAll(self):
        dict = []
        allItems = []
        collection = self.db[self.collection]
        response = collection.find()
        for i in response:
            i['_id'] = str(i['_id'])
            i['asesor'] = str(i['asesor'])
            i['Producto'] = str(i['Producto'])
            i['Cliente'] = str(i['Cliente'])
            allItems.append(i)
        dict.append(allItems)
        return dict

    def getById(self, id):
        try:
            dict = []
            collection = self.db[self.collection]
            response = collection.find_one({"_id": ObjectId(id)})
            response['_id'] = str(response['_id'])
            response['asesor'] = str(response['asesor'])
            response['Producto'] = str(response['Producto'])
            response['Cliente'] = str(response['Cliente'])
            dict.append(response)
            return dict
        except:
            return {"status": False , "code": 400, "message": "no se encontro el id " + id}

    def update(self, id, infoUpdate):
            dict = []
            collection = self.db[self.collection]
            infoUpdate = infoUpdate.__dict__
            print(id)
            collection.update_one({"_id": ObjectId(id)}, {"$set": infoUpdate})
            response = collection.find_one({"_id": ObjectId(id)})
            response['_id'] = str(response['_id'])
            response['asesor'] = str(response['asesor'])
            response['Producto'] = str(response['Producto'])
            response['Cliente'] = str(response['Cliente'])
            dict.append(response)
            return dict


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
            x['Cliente'] = str(x['Cliente'])
        x = self.transformObjectIds(x)
        x = self.getValuesDBRef(x)
        data.append(x)
        return data