from repositories.interfaceRepositorio import interfaceRepositorio
from models.tareaModisteria import tareaModisteria
from bson import ObjectId,DBRef

class repoTareaModista(interfaceRepositorio[tareaModisteria]):
    def save(self, item: tareaModisteria):
        print("def save")
        collection = self.db[self.collection]
        inserted = collection.insert_one(item.__dict__)
        id = inserted.inserted_id.__str__()
        print(id)
        response = collection.find_one({"_id": ObjectId(id)})
        response['_id'] = str(response['_id'])
        response['formMedidas'] = str(response['formMedidas'])
        response['producto'] = str(response['producto'])
        if response['modista'] is not None:
            response['modista'] = str(response['modista'])
        return response


    def getAll(self):
        dict = []
        allItems = []
        collection = self.db[self.collection]
        response = collection.find()
        for i in response:
            i['_id'] =str(i['_id'])
            i['formMedidas'] = str(i['formMedidas'])
            i['modista'] = str(i['modista'])
            i['producto'] = str(i['producto'])
            allItems.append(i)
        dict.append(allItems)
        return dict

    def getById(self, id):
        collection = self.db[self.collection]
        response = collection.find_one({"_id":ObjectId(id)})
        if response != None:
            response['_id'] = str(response['_id'])
            response['formMedidas'] = str(response['formMedidas'])
            response['modista'] = str(response['modista'])
            response['producto'] = str(response['producto'])
        return response

    def getByIdToUpdate(self,id):
        collection = self.db[self.collection]
        response = collection.find_one({"_id":ObjectId(id)})
        return response
    def update(self,id , item:tareaModisteria):
        try:
            dict = []
            collection = self.db[self.collection]
            item = item.__dict__
            print(id)
            collection.update_one({"_id":ObjectId(id)},{"$set":item})
            response = collection.find_one({"_id": ObjectId(id)})
            response['_id'] = str(response['_id'])
            response['formMedidas'] = str(response['formMedidas'])
            response['modista'] = str(response['modista'])
            response['producto'] = str(response['producto'])
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

    def getTareasPendientes(self,idModista):
        allItems = []
        collection = self.db[self.collection]
        query = {"$and": [{"modista": DBRef("empleado", ObjectId(idModista))},{"completado": False}]}
        response = collection.find(query)
        for item in response:
            if item is not None:
                item['_id'] = str(item['_id'])
                item['formMedidas'] = str(item['formMedidas'])
                item['modista'] = str(item['modista'])
                item['producto'] = str(item['producto'])
                allItems.append(item)
        return allItems

    def getTareasSinAsignar(self):
        allItems = []
        collection = self.db[self.collection]
        response = collection.find({"modista":None})
        for item in response:
            if item is not None:
                item['_id'] = str(item['_id'])
                item['formMedidas'] = str(item['formMedidas'])
                item['producto'] = str(item['producto'])
                allItems.append(item)
        return allItems

    pass