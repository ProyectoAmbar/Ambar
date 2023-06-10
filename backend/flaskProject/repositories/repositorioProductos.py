from repositories.interfaceRepositorio import interfaceRepositorio
from models.producto import Producto


class RepositorioProductos(interfaceRepositorio[Producto]):
    def getByReferencia(self, ref):
        collection = self.db[self.collection]
        response = collection.find_one({"referencia": ref})
        if response:
            return True
        else:
            return False

    def getByNombre(self, nombre):
        collection = self.db[self.collection]
        response = collection.find_one({"nombre": nombre})
        if response:
            return True
        else:
            return False
    pass
