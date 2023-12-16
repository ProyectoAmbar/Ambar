from repositories.interfaceRepositorio import interfaceRepositorio
from bson import ObjectId, DBRef
from models.FormatoMedidas import formatoMedidas

class repositorioFormMedidas(interfaceRepositorio[formatoMedidas]):
    def save(self, item: formatoMedidas):
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
        return response


    def getAll(self):
        allItems = []
        collection = self.db[self.collection]
        response = collection.find()
        for i in response:
            i['_id'] =str(i['_id'])
            i['asesor'] = str(i['asesor'])
            i['producto'] = str(i['producto'])
            i['formulario'] = str(i['formulario'])
            allItems.append(i)
        return allItems

    def getById(self, id):
        collection = self.db[self.collection]
        response = collection.find_one({"_id":ObjectId(id)})
        if response != None:
            response['_id'] = str(response['_id'])
            response['asesor'] = str(response['asesor'])
            response['producto'] = str(response['producto'])
            response['formulario'] = str(response['formulario'])
        return response

    def getByIdToUpdate(self,id):
        collection = self.db[self.collection]
        response = collection.find_one({"_id": ObjectId(id)})
        return response

    def getFormMedidasByFormAlquiler(self, idFormAlquiler:str):
        collection = self.db[self.collection]
        response = collection.find_one({"formulario": DBRef('formatoAlquiler', ObjectId(idFormAlquiler))})
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

    pass
