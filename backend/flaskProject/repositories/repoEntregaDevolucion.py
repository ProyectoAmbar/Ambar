from repositories.interfaceRepositorio import interfaceRepositorio
from models.entregaDevolucion import entregaDevolucion
from bson import DBRef,ObjectId
class repoEntregaDevolucion(interfaceRepositorio[entregaDevolucion]):
    def save(self, item: entregaDevolucion):
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
        dict.append(response)
        return dict

    def getAllSinEntregar(self):
        allItems = []
        collection = self.db[self.collection]
        response = collection.find({"entregaCompletado": False})
        for i in response:
            i['_id'] = str(i['_id'])
            i['asesor'] = str(i['asesor'])
            i['producto'] = str(i['producto'])
            allItems.append(i)
        return allItems

    def getAllSinDevolver(self):
        allItems = []
        collection = self.db[self.collection]
        query = {"$and": [{"entregaCompletado": True}, {"devolucionCompletado": False}]}
        response = collection.find(query)
        for i in response:
            i['_id'] = str(i['_id'])
            i['asesor'] = str(i['asesor'])
            i['producto'] = str(i['producto'])
            allItems.append(i)
        return allItems



    def getAll(self):
        allItems = []
        collection = self.db[self.collection]
        response = collection.find()
        for i in response:
            i['_id'] =str(i['_id'])
            i['asesor'] = str(i['asesor'])
            i['producto'] = str(i['producto'])
            allItems.append(i)
        return allItems

    def getById(self, id):
        collection = self.db[self.collection]
        response = collection.find_one({"_id":ObjectId(id)})
        if response != None:
            response['_id'] = str(response['_id'])
            response['asesor'] = str(response['asesor'])
            response['producto'] = str(response['producto'])
        return response

    def getByIdToUpdate(self,id):
        collection = self.db[self.collection]
        response = collection.find_one({"_id": ObjectId(id)})
        return response
    def update(self,id , item:entregaDevolucion):
        try:
            collection = self.db[self.collection]
            item = item.__dict__
            print(id)
            collection.update_one({"_id":ObjectId(id)},{"$set":item})
            response = collection.find_one({"_id": ObjectId(id)})
            response['_id'] = str(response['_id'])
            response['asesor'] = str(response['asesor'])
            response['producto'] = str(response['producto'])
            return response
        except:
            dict = [{
                "status": False,
                "code": 403,
                "message": "no se encontro el id"
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
