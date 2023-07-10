from models.producto import Producto
from repositories.repositorioProductos import RepositorioProductos


class ProductoController():
    def __init__(self):
        self.RepositorioProductos = RepositorioProductos()

    def create(self, infoProducto):
        try:
            if infoProducto['nombre'] and infoProducto['referencia'] and infoProducto['imagenProducto'] and infoProducto['cantidadTallaS'] and infoProducto['cantidadTallaM'] and infoProducto['cantidadTallaL']:
                theProduct = Producto(infoProducto)
                print(theProduct)
                productoPorReferencia = self.RepositorioProductos.getByReferencia(theProduct.referencia)
                productoPorNombre = self.RepositorioProductos.getByNombre(theProduct.nombre)
                if not productoPorNombre and not productoPorReferencia:
                    response = self.RepositorioProductos.save(theProduct)
                    response.append({"status": True, "code": 200, "message": "El producto fue agregado a la base de datos con exito"})
                    return response
                else:
                    return {"status": False, "code": 400, "message": "ya existe un con la referencia dada o el mismo nombre de producto"}
        except:
            return {"status": False, "code": 400, "message": "el producto no pudo ser creado"}

    def getAllProducts(self):
        print("get all products")
        return self.RepositorioProductos.getAll()

    def getById(self,id):
        print("mostrando producto con : ", id)
        response =  self.RepositorioProductos.getById(id)
        if response[0] != None:
            return response
        else:
            return {"status": False , "code": 400, "message": "No se encontro el producto con id: " + id}

    def getByRef(self,referencia):
        print("mostrando prodcuto con referencia: "+ referencia)
        response = self.RepositorioProductos.getByReferencia(referencia)
        if response != None:
            return response
        else:
            return {"status": False, "code": 400, "message": "No se encontro el producto con referencia: " + referencia}


    def updateProduct(self, _id, infoProducto):
        print("actualizando un producto")
        if infoProducto["nombre"] and infoProducto["referencia"] and infoProducto["imagenProducto"] and infoProducto["cantidadTallaS"] and infoProducto["cantidadTallaM"] and infoProducto["cantidadTallaL"]:
            search = self.RepositorioProductos.getByReferencia(infoProducto["referencia"])
            print(search)
            if not search or str(search["_id"]) == _id:
                response = self.RepositorioProductos.update(_id, Producto(infoProducto))
                response.append({"status": True, "code": 200, "message": "el producto fue actualizado"})
                return response
            else:
                return {"status": False, "Code": 400, "message": "hace falta información o el id no fue encontrado"}


    def deleteProducto(self, _id):
        print("eliminar un producto")


        return self.RepositorioProductos.delete(_id)


