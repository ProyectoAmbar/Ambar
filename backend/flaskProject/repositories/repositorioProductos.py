from repositories.interfaceRepositorio import interfaceRepositorio
from models.producto import Producto


class RepositorioProductos(interfaceRepositorio[Producto]):
    def getByReferencia(self, ref):
        print(ref)
        dict = []
        collection = self.db[self.collection]
        response = collection.find_one({"referencia": ref})
        if response != None:
            response['_id'] = str(response['_id'])
            return response
        else:
            return None

    def getByNombre(self, nombre):
        collection = self.db[self.collection]
        response = collection.find_one({"nombre": nombre})
        if response:
            return response
        else:
            return None
    pass