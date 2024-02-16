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

    def extract_date(self, item):
        date_keys = ["fecha", "fechaCitaDeMedidas", "fechaEntrega", "fechaDevolucion"]
        for i in item:
            for key in date_keys:
                value = i.get(key)
                if value:
                    # Check if the value is already a datetime object
                    if isinstance(value, datetime):
                        return value
                    # If it's a string, parse it to a datetime object
                    elif isinstance(value, str):
                        try:
                            return datetime.strptime(value, "%Y-%m-%d")
                        except ValueError:
                            # Handle the case where the string date is not in the expected format
                            # You can modify this part based on your specific needs
                            print(f"Error parsing date: {value}")

        # If none of the keys exist or couldn't be parsed, return a default value
        return datetime.min

    def tareasEnOrdenPorFecha(self):
        tareasOrdenadas = []
        asesor = self.tareaAsesor.getAllTareasPendientes()
        modista = self.tareaModista.getAllTareasModistaPendientes()
        lavanderia = self.tareaLavanderia.getAllPendientes()
        entrega = self.entregaDevolucion.getSinEntregar()
        devolucion = self.entregaDevolucion.getSinDevolver()
        fotos = self.fotos.getSinCompletar()
        makeup = self.makeup.getAllPendientes()
        cita = self.primeraCita.getSinCompletar()
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
        extract_date = lambda item: self.extract_date(tareasOrdenadas)

        sorted_data = sorted(tareasOrdenadas, key=extract_date)
        return sorted_data

    def calendarAsesor(self,idAsesor):
        tareasOrdenadas = []
        tarea = self.tareaAsesor.verTareasPendientesPorAsesor(idAsesor)
        entrega = self.entregaDevolucion.getSinEntregarByAsesor(idAsesor)
        devolucion = self.entregaDevolucion.getSinDevolverByAsesor(idAsesor)
        cita = self.primeraCita.getSinCompletar()
        for i in tarea:
            tareasOrdenadas.append(i)
        for i in entrega:
            tareasOrdenadas.append(i)
        for i in devolucion:
            tareasOrdenadas.append(i)
        for i in cita:
            tareasOrdenadas.append(i)

        extract_date = lambda item: self.extract_date(tareasOrdenadas)

        sorted_data = sorted(tareasOrdenadas, key=extract_date)
        return sorted_data
