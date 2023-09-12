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
        response['formulario'] = str(response['formulario'])
        response['asesor'] = str(response['asesor'])
        response['producto'] = str(response['producto'])
        return response

    def getAllSinEntregar(self):
        allItems = []
        collection = self.db[self.collection]
        response = collection.find({"entregaCompletado": False}).sort("fechaEntrega",1)
        for i in response:
            i['_id'] = str(i['_id'])
            i['asesor'] = str(i['asesor'])
            i['formulario'] = str(i['formulario'])
            i['producto'] = str(i['producto'])
            allItems.append(i)
        return allItems

    def getAllSinDevolver(self):
        allItems = []
        collection = self.db[self.collection]
        query = {"$and": [{"entregaCompletado": True}, {"devolucionCompletado": False}]}
        response = collection.find(query).sort("fechaDevolucion",1)
        for i in response:
            i['_id'] = str(i['_id'])
            i['asesor'] = str(i['asesor'])
            i['formulario'] = str(i['formulario'])
            i['producto'] = str(i['producto'])
            allItems.append(i)
        return allItems


    def getAllSinEntregarByAsesor(self,idAsesor:str):
        allItems = []
        collection = self.db[self.collection]
        query = {"$and":[{"entregaCompletado":False},{"asesor": DBRef('empleado', ObjectId(idAsesor))}]}
        response = collection.find(query)
        for i in response:
            i['_id'] = str(i['_id'])
            i['asesor'] = str(i['asesor'])
            i['formulario'] = str(i['formulario'])
            i['producto'] = str(i['producto'])
            allItems.append(i)
        return allItems

    def getAllSinDevolverByAsesor(self,idAsesor:str):
        allItems = []
        collection = self.db[self.collection]
        query = {"$and": [{"entregaCompletado": True}, {"devolucionCompletado": False}, {"asesor": DBRef('empleado', ObjectId(idAsesor))}]}
        response = collection.find(query)
        for i in response:
            i['_id'] = str(i['_id'])
            i['asesor'] = str(i['asesor'])
            i['formulario'] = str(i['formulario'])
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
            i['formulario'] = str(i['formulario'])
            i['producto'] = str(i['producto'])
            allItems.append(i)
        return allItems

    def getById(self, id):
        collection = self.db[self.collection]
        response = collection.find_one({"_id":ObjectId(id)})
        try:
            if response != None:
                response['_id'] = str(response['_id'])
                response['asesor'] = str(response['asesor'])
                response['formulario'] = str(response['formulario'])
                response['producto'] = str(response['producto'])
            return response
        except:
            return {"status": False, "code": 400, "message": "no se encontro la Entrega/Devolución"}

    def getByFormulario(self,formulario):
        collection = self.db[self.collection]
        response = collection.find_one({'formulario': DBRef('formatoAlquiler', ObjectId(formulario))})
        try:
            if response != None:
                response['_id'] = str(response['_id'])
                response['asesor'] = str(response['asesor'])
                response['formulario'] = str(response['formulario'])
                response['producto'] = str(response['producto'])
            return response
        except:
            return {"status": False, "code": 400, "message": "no se encontro la Entrega/Devolución"}

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
            response['formulario'] = str(response['formulario'])
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
        collection = self.db[self.collection]
        delObject = collection.delete_one({'_id':ObjectId(id)}).deleted_count
        return {"deleted_count": delObject}
