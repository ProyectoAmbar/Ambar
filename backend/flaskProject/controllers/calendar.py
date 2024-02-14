from controllers.TareaController import tareaController
from controllers.tareaModistaController import tareaModisteriaController
from controllers.lavanderiaController import lavanderiaController
from controllers.entregaDevolucionController import entregaDevolucionController
from controllers.fotosController import fotosController
from controllers.tareaMakeUpController import tareaMakeupController
from controllers.primeraVezController import primeraVezController
from datetime import datetime

class calendar():
    def __init__(self):
        self.tareaAsesor = tareaController()
        self. tareaModista = tareaModisteriaController()
        self.tareaLavanderia = lavanderiaController()
        self.entregaDevolucion = entregaDevolucionController()
        self.fotos = fotosController()
        self.makeup = tareaMakeupController()
        self.primeraCita = primeraVezController()


    def tareasEnOrdenPorFecha(self):
        tareasOrdenadas = []
        asesor = self.tareaAsesor.getAllTareasPendientes()
        modista = self.tareaModista.getAllTareasModistaPendientes()
        lavanderia = self.tareaLavanderia.getAllPendientes()
        entrega = self.entregaDevolucion.getSinEntregar()
        devolucion = self.entregaDevolucion.getSinDevolver()
        fotos = self.fotos.getSinCompletar()
        makeup = self.makeup.getAllPendientes()
        cita = primeraVezController.getSinCompletar()
        for i in asesor:
            tareasOrdenadas.append(i)
        for i in modista:
            tareasOrdenadas.append(i)
        for i in lavanderia:
            tareasOrdenadas.append(i)
        for i in entrega:
            tareasOrdenadas.append(i)
        for i in devolucion:
            tareasOrdenadas.append(i)
        for i in fotos:
            tareasOrdenadas.append(i)
        for i in makeup:
            tareasOrdenadas.append(i)
        for i in cita:
            tareasOrdenadas.append(i)
        extract_date = lambda item: item.get("fecha") or item.get("fechaCitaDeMedidas") or item.get(
            "fechaEntrega") or item.get("fechaDevolucion")

        sorted_data = sorted(tareasOrdenadas, key=lambda item: datetime.strptime(extract_date(item), "%Y-%m-%d"))
        return sorted_data

    def calendarAsesor(self,idAsesor):
        tareasOrdenadas = []
        tarea = self.tareaAsesor.verTareasPendientesPorAsesor(idAsesor)
        entrega = self.entregaDevolucion.getSinEntregarByAsesor(idAsesor)
        devolucion = self.entregaDevolucion.getSinDevolverByAsesor(idAsesor)
        cita = primeraVezController.getSinCompletar()
        for i in tarea:
            tareasOrdenadas.append(i)
        for i in entrega:
            tareasOrdenadas.append(i)
        for i in devolucion:
            tareasOrdenadas.append(i)
        for i in cita:
            tareasOrdenadas.append(i)

        extract_date = lambda item: item.get("fecha") or item.get("fechaCitaDeMedidas") or item.get(
            "fechaEntrega") or item.get("fechaDevolucion")

        sorted_data = sorted(tareasOrdenadas, key=lambda item: datetime.strptime(extract_date(item), "%Y-%m-%d"))
        return sorted_data
