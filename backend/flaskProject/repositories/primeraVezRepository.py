from repositories.interfaceRepositorio import interfaceRepositorio
from models.citaPrimeraVez import citaPrimeraVez
from bson import ObjectId, DBRef
from datetime import datetime
class primeraVezRepository(interfaceRepositorio[citaPrimeraVez]):
    def save(self,infoCita):
        collection = self.db[self.collection]
        inserted = collection.insert_one(infoCita.__dict__)
        id = inserted.inserted_id.__str__()
        print(id)
        response = collection.find_one({"_id": ObjectId(id)})
        response['_id'] = str(response['_id'])
        response['asesor'] = str(response['asesor'])
        return response

    def getAll(self):
        allItems = []
        collection = self.db[self.collection]
        response = collection.find()
        for i in response:
            i['_id'] =str(i['_id'])
            i['asesor'] = str(i['asesor'])
            allItems.append(i)
        return allItems

    def getById(self, id):
        collection = self.db[self.collection]
        response = collection.find_one({"_id": ObjectId(id)})
        if response != None:
            response['_id'] = str(response['_id'])
            response['asesor'] = str(response['asesor'])
            return response
        else:
            return None

    def update(self,id , infoCita):
        try:
            collection = self.db[self.collection]
            infoCita = infoCita.__dict__
            print(id)
            collection.update_one({"_id":ObjectId(id)},{"$set":infoCita})
            response = collection.find_one({"_id": ObjectId(id)})
            response['_id'] = str(response['_id'])
            response['asesor'] = str(response['asesor'])
            return response
        except:
            dict = [{
                "status": False,
                "code": 403,
                "message": "La cita con id "+id+" no ha sido encontrada"
            }]
            return dict

    def getCitasSinCompletar(self):
        allItems = []
        collection = self.db[self.collection]
        query = {"estado": False}
        print(query)
        response = collection.find(query).sort("fecha", 1)
        for item in response:
            if item is not None:
                item['_id'] = str(item['_id'])
                item['asesor'] = str(item['asesor'])
                allItems.append(item)
        return allItems

    def getCitaSinCompletarByAsesor(self,id):
        allItems = []
        collection = self.db[self.collection]
        query = {
            "$and": [
                {"estado": False},
                {"asesor": DBRef("empleado", ObjectId(id))}
            ]
        }
        print(query)
        response = collection.find(query).sort("fecha", 1)
        for item in response:
            if item is not None:
                item['_id'] = str(item['_id'])
                item['asesor'] = str(item['asesor'])
                allItems.append(item)
        return allItems

    def getCitasSinAsignar(self):
        allItems = []
        collection = self.db[self.collection]
        query = {
            "$and": [
                {"estado": False},
                {"asesor": None}
            ]
        }
        print(query)
        response = collection.find(query).sort("fecha", 1)
        for item in response:
            if item is not None:
                item['_id'] = str(item['_id'])
                item['asesor'] = str(item['asesor'])
                allItems.append(item)
        return allItems

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
    pass




