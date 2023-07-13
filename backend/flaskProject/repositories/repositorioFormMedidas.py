from repositories.interfaceRepositorio import interfaceRepositorio
from bson.objectid import ObjectId
from models.FormatoMedidas import formatoMedidas

class repositorioFormMedidas(interfaceRepositorio[formatoMedidas]):
    def save(self, item: formatoMedidas):
        dict = []
        print("def save")
        collection = self.db[self.collection]
        inserted = collection.insert_one(item.__dict__)
        id = inserted.inserted_id.__str__()
        print(id)
        response = collection.find_one({"_id": ObjectId(id)})
        response['_id'] = str(response['_id'])
        response['asesor'] = str(response['asesor'])
        response['producto'] = str(response['producto'])
        response['formulario'] = str(response['formulario'])

        dict.append(response)
        return dict


    def getAll(self):
        dict = []
        allItems = []
        collection = self.db[self.collection]
        response = collection.find()
        for i in response:
            i['_id'] =str(i['_id'])
            i['asesor'] = str(i['asesor'])
            i['producto'] = str(i['producto'])
            i['formulario'] = str(i['formulario'])
            allItems.append(i)
        dict.append(allItems)
        return dict

    def getById(self, id):
        collection = self.db[self.collection]
        response = collection.find_one({"_id":ObjectId(id)})
        if response != None:
            response['_id'] = str(response['_id'])
            response['asesor'] = self.db['empleado'].find_one({"_id": response['asesor']})
            response['producto'] = self.db['Producto'].find_one({"_id": response['asesor']})
            response['formulario'] = self.db['formatoAlquiler'].find_one({"_id": response['formulario']})
        return response

    def getByIdToUpdate(self,id):
        collection = self.db[self.collection]
        response = collection.find_one({"_id": ObjectId(id)})
        return response
    def update(self,id , item:formatoMedidas):
        try:
            dict = []
            collection = self.db[self.collection]
            item = item.__dict__
            print(id)
            collection.update_one({"_id":ObjectId(id)},{"$set":item})
            response = collection.find_one({"_id": ObjectId(id)})
            response['_id'] = str(response['_id'])
            response['asesor'] = str(response['asesor'])
            response['producto'] = str(response['producto'])
            response['formulario'] = str(response['formulario'])

            dict.append(response)
            return response
        except:
            dict = [{
                "status": False,
                "code": 403,
                "message": "El candidato con id "+id+" no ha sido encontrado"
            }]
            return dict


    def delete(self,id):
        dict = [{
            "status": True,
            "code": 202
        }]
        collection = self.db[self.collection]
        delObject = collection.delete_one({'_id':ObjectId(id)}).deleted_count
        dict.append({"deleted_count": delObject})
        return dict
