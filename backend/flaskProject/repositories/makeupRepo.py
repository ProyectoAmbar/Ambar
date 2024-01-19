from models.FormatoMakeup import formatoMakeUP
from repositories.interfaceRepositorio import interfaceRepositorio
from bson import ObjectId
from datetime import datetime, timedelta

class makeupRepo(interfaceRepositorio[formatoMakeUP]):
    def save(self, formAlquiler):
        print("def save")
        collection = self.db[self.collection]
        inserted = collection.insert_one(formAlquiler.__dict__)
        id = inserted.inserted_id.__str__()
        print(id)
        response = collection.find_one({"_id": ObjectId(id)})
        print(response)
        response['_id'] = str(response['_id'])
        response['maquilladora'] = str(response['maquilladora'])

        return response

    def getAll(self):
        allItems = []
        collection = self.db[self.collection]
        response = collection.find()
        for i in response:
            i['_id'] = str(i['_id'])
            i['maquilladora'] = str(i['maquilladora'])
            allItems.append(i)
        return allItems

    def getById(self, id):
        try:
            collection = self.db[self.collection]
            response = collection.find_one({"_id": ObjectId(id)})
            response['_id'] = str(response['_id'])
            response['maquilladora'] = str(response['maquilladora'])

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
            response['maquilladora'] = str(response['maquilladora'])
            return response

    def getByIdToUpdate(self, id):
            collection = self.db[self.collection]
            response = collection.find_one({"_id": ObjectId(id)})
            return response

    def getTareasPorDia(self, año,mes,dia):
        dict = []
        collection = self.db[self.collection]
        hora1 = datetime(año,mes,dia,0,0,0)
        hora2 = datetime(año,mes,dia,23,59,59)
        response = collection.find({"fecha_hora": {"$gte": hora1,"$lte": hora2}})
        for i in response:
            i['_id'] = str(i['_id'])
            i['maquilladora'] = str(i['maquilladora'])
            dict.append(i)
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

    def getByFactura(self,Factura):
        try:
            collection = self.db[self.collection]
            response = collection.find_one({'fv': Factura})
            response['_id'] = str(response['_id'])
            response['maquilladora'] = str(response['maquilladora'])

            return response
        except:
            return {"status": False , "code": 400, "message": "no se encontro el form de factura numero " + Factura}

    def query(self, theQuery):
        dict=[]
        collection = self.db[self.collection]
        response = collection.find(theQuery)
        for i in response:
            i['_id'] = str(i['_id'])
            i['maquilladora'] = str(i['maquilladora'])
            dict.append(i)
        return dict