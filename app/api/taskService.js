import axios from 'axios';
import API_URLS from './services';
import Cookies from 'js-cookie';

export const AllTaskPending = async () => {
    const response = await axios.get(`${API_URLS.microservicio3}/calendar`);
    console.log(response.data);
    return response.data;
};


export const TaskCitaPrimera = async () => {
    try {
        const token = Cookies.get('Token');

        const response = await axios.get(`${API_URLS.microservicio1}/cita`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error('Error al obtener las tareas:', error);
        throw error;
    }
};

export const MakeupTask = async () => {
    try {
        const token = Cookies.get('Token');

        const response = await axios.get(`${API_URLS.microservicio3}/tareaMakeup`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error('Error al obtener las tareas Make Up:', error);
        throw error;
    }
}

export const PhotoTask = async () => {
    try {
        const token = Cookies.get('Token');

        const response = await axios.get(`${API_URLS.microservicio3}/fotos`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error('Error al obtener las tareas Make Up:', error);
        throw error;
    }
}

// All tasks of different different roles, to represent a content in the view

export const AllTaskModista = async () => {
    const response = await axios.get(`${API_URLS.microservicio3}/tareaModista`);
    console.log(response.data);
    return response.data;
}

export const AllTaskLavanderia = async () => {
    const response = await axios.get(`${API_URLS.microservicio3}/lavanderia`);
    console.log(response.data);
    return response.data;
}


export const AllGeneralTask = async () => {
    try {
        const token = Cookies.get('Token');

        const response = await axios.get(`${API_URLS.microservicio1}/tarea`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error('Error al obtener las tareas:', error);
        throw error;
    }
};

//Funcion para extraer objeto
export const extractIdFromDBRef = (dbRefString) => {
    const matches = dbRefString.match(/ObjectId\('([^']+)'\)/);
    return matches ? matches[1] : null;
};


//Metodos para Traer tareas y datos de asesor
export const getTasksForRoleAsesor = async () => {
    try {
        const token = Cookies.get('Token');
        const IdEmpleado = Cookies.get('idEmpleado');

        const response = await axios.get(`${API_URLS.microservicio1}/tarea/verPendientes/${IdEmpleado}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error('Error al obtener las tareas:', error);
        throw error;
    }
};

export const getTasksForRoleAsesorCita = async () => {
    try {
        const token = Cookies.get('Token');
        const IdEmpleado = Cookies.get('idEmpleado');

        const response = await axios.get(`${API_URLS.microservicio3}/cita/sinCompletar`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error('Error al obtener las tareas De cita primera vez:', error);
        throw error;
    }
}

export const fetchAsesorName = async (dbRefAsesor) => {
    const idAsesor = extractIdFromDBRef(dbRefAsesor);
    if (!idAsesor) throw new Error("ID de asesor no válido");
    const response = await axios.get(`${API_URLS.microservicio2}/empleado/${idAsesor}`);
    console.log(response.data);
    return response.data;
};
export const fetchmakeupbyUserid = async (dbRefAsesor) => {
    const idAsesor = extractIdFromDBRef(dbRefAsesor);
    if (!idAsesor) throw new Error("ID de makeup no válido");
    const response = await axios.get(`${API_URLS.microservicio2}/empleado/getByUser/${idAsesor}`);
    console.log(response.data);
    return response.data;
};

export const fetchProductoName = async (dbRefProducto) => {
    const idProducto = extractIdFromDBRef(dbRefProducto);
    if (!idProducto) throw new Error("ID de producto no válido");

    try {
        const token = Cookies.get('Token');
        const response = await axios.get(`${API_URLS.microservicio1}/productos/getById/${idProducto}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error('Error al obtener las tareas:', error);
        throw error;
    }
};

export const fetchProductoName2 = async (idProducto) => {
    try {
        const token = Cookies.get('Token');
        const response = await axios.get(`${API_URLS.microservicio3}/productos/getReferencia/${idProducto}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error('Error al obtener las tareas:', error);
        throw error;
    }
};

export const getTareaCitaMedidasById = async () => {
    const idTareaCitaMedidas = Cookies.get('IdCitaMedidas');
    const response = await axios.get(`${API_URLS.microservicio3}/tarea/${idTareaCitaMedidas}`);
    console.log(response.data);
    return response.data;
};

export const getFormByCitaMedidas = async (dbRefFormulario) => {
    const dbRefFormu = extractIdFromDBRef(dbRefFormulario);
    if (!dbRefFormu) throw new Error("ID de producto no válido");

    try {
        const token = Cookies.get('Token');
        const response = await axios.get(`${API_URLS.microservicio1}/alquiler/${dbRefFormu}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error('Error al obtener las tareas:', error);
        throw error;
    }
};

export const getAsesorByCita = async (dbrefAsesor) => {
    const idAsesor = extractIdFromDBRef(dbrefAsesor);
    if (!idAsesor) throw new Error("ID de asesor no válido");
    const response = await axios.get(`${API_URLS.microservicio2}/empleado/${idAsesor}`);
    console.log(response.data);
    return response.data;
};

export const getProductobyCita = async (dbrefProduct) => {
    const dbReproduc = extractIdFromDBRef(dbrefProduct);
    if (!dbReproduc) throw new Error("ID de producto no válido");

    try {
        const token = Cookies.get('Token');
        const response = await axios.get(`${API_URLS.microservicio1}/productos/getById/${dbReproduc}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error('Error al obtener las tareas:', error);
        throw error;
    }
};
// Fin Metodos para Traer tareas y datos de asesor

// Asignar Tareas Metodos
export const getTareasDontAsing = async () => {
    try {
        const token = Cookies.get('Token');
        const response = await axios.get(`${API_URLS.microservicio1}/tareaModista/sinAsignar`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error('Error al obtener las tareas:', error);
        throw error;
    }

}

export const getAllEmployees = async () => {
    try {
        const token = Cookies.get('Token');

        const response = await axios.get(`${API_URLS.microservicio1}/empleado`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error('Error al obtener las tareas:', error);
        throw error;
    }
};


export const updateTaskWithWorker = async (taskId, data) => {
    try {
        const token = Cookies.get('Token');

        const response = await axios.put(`${API_URLS.microservicio1}/tareaModista/asignar/${taskId}`, data, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        return response.data;
    } catch (error) {
        console.error('Error en updateTaskWithWorker:', error);
        throw error;
    }
};

//Fin metodos Asignar

//Metodos para Traer tareas y datos de Modista
export const getTasksForRoleModista = async () => {
    try {
        const token = Cookies.get('Token');
        const IdEmpleado = Cookies.get('idEmpleado');

        const response = await axios.get(`${API_URLS.microservicio3}/tareaModista/pendientes/${IdEmpleado}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error('Error al obtener las tareas:', error);
        throw error;
    }
};

export const fetchModistaName = async (dbRefAsesor) => {
    const idAsesor = extractIdFromDBRef(dbRefAsesor);
    if (!idAsesor) throw new Error("ID de asesor no válido");
    const response = await axios.get(`${API_URLS.microservicio2}/empleado/${idAsesor}`);
    console.log(response.data);
    return response.data;
};

// Medoso Modista para responder y mostrar arreglos en sastreria

export const getInfoArregloModista = async () => {
    try {
        const token = Cookies.get('Token');
        const IdTareaArregloModista = Cookies.get('IdTareaModista');
        const response = await axios.get(`${API_URLS.microservicio1}/tareaModista/${IdTareaArregloModista}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error('Error al obtener la tarea para arreglar de modista:', error);
        throw error;
    }
};


export const getModistaArreglos = async (dbRefFormMedidas) => {
    const refFormMedidas = extractIdFromDBRef(dbRefFormMedidas);
    const response = await axios.get(`${API_URLS.microservicio3}/formMedidas/${refFormMedidas}`);
    console.log(response.data);
    return response.data;
}

//Metodos Asignar A lavanderia 

export const getTareasDontAsingLavanderia = async () => {
    try {
        const token = Cookies.get('Token');
        const response = await axios.get(`${API_URLS.microservicio1}/lavanderia/sinAsignar`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error('Error al obtener las tareas:', error);
        throw error;
    }

}


export const updateTaskWithWorkerLavanderia = async (taskId, data) => {
    try {
        const token = Cookies.get('Token');
        const response = await axios.put(`${API_URLS.microservicio1}/lavanderia/${taskId}/empleado/${data.lavanderia}`, {}, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        return response.data;
    } catch (error) {
        console.error('Error en updateTaskWithWorker Lavanderia:', error);
        throw error;
    }

};

//Ver Tareas de Lavanderia

export const fetchLavanderiaName = async (dbRefAsesor) => {
    const idAsesor = extractIdFromDBRef(dbRefAsesor);
    if (!idAsesor) throw new Error("ID de asesor no válido");
    const response = await axios.get(`${API_URLS.microservicio2}/empleado/${idAsesor}`);
    console.log(response.data);
    return response.data;
};

export const getTasksForRoleLavanderia = async () => {
    try {
        const token = Cookies.get('Token');
        const IdEmpleado = Cookies.get('idEmpleado');

        const response = await axios.get(`${API_URLS.microservicio3}/lavanderia/pendientes/${IdEmpleado}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error('Error al obtener las tareas:', error);
        throw error;
    }
};


export const GetTareaLavanderia = async () => {
    const idTareaLavanderia = Cookies.get('IdTareaLavanderia');
    const response = await axios.get(`${API_URLS.microservicio3}/lavanderia/${idTareaLavanderia}`);
    console.log(response.data);
    return response.data;
};

export const getformAlquiler = async (dbrefIdForm) => {
    const form = extractIdFromDBRef(dbrefIdForm);
    const response = await axios.get(`${API_URLS.microservicio1}/alquiler/${form}`);
    console.log(response.data);
    return response.data;
};

// Function for Create and Update user info

export const createEmployee = async (formData, idRolselected) => {
    const token = Cookies.get('Token');
    const response = await axios.post(`${API_URLS.microservicio1}/empleado/rol/${idRolselected}`, formData, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    console.log(response)
    return response.data;
};

export const updateEmployee = async (id, values) => {
    try {
        const token = Cookies.get('Token');

        const response = await axios.put(`${API_URLS.microservicio1}/empleado/${id}`, values, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        console.log(response.data)
        return response.data;
    } catch (error) {
        console.error('Error en updateTaskWithWorker:', error);
        throw error;
    }
};

export const getEmployeeDataById = async (idEmployee) => {
    try {
        const token = Cookies.get('Token');

        const response = await axios.get(`${API_URLS.microservicio1}/empleado/${idEmployee}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error('Error al obtener la info del Empleado:', error);
        throw error;
    }
};

export const deleteEmployeeById = async (idEmployee) => {
    const Token = Cookies.get('Token');
    try {
        const response = await axios.delete(`${API_URLS.microservicio1}/empleado/${idEmployee}`, {
            headers: {
                'Authorization': `Bearer ${Token}`
            }
        });
        console.log('Respuesta de eliminación:', response);
        return response.data;
    } catch (error) {
        console.error('Error al eliminar el empleado', error);
        throw error;
    }
};

// Service for a response at Deliver and Returns

export const getAllDeliver = async () => {
    const response = await axios.get(`${API_URLS.microservicio3}/entregaDevolucion/SinEntregar`);
    console.log(response.data);
    return response.data;
}

export const getAllReturns = async () => {
    const response = await axios.get(`${API_URLS.microservicio3}/entregaDevolucion/SinDevolver`);
    console.log(response.data);
    return response.data;
}

export const updateTaskResponse = async (idTask, data) => {
    try {
        const token = Cookies.get('Token');

        const response = await axios.put(`${API_URLS.microservicio1}/entregaDevolucion/entrega/${idTask}`, data, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        return response.data;
    } catch (error) {
        console.error('Error en Entregar Producto a Cliente:', error);
        throw error;
    }
}

export const updateResponseReturn = async (idTask, data) => {
    try {
        const token = Cookies.get('Token');

        const response = await axios.put(`${API_URLS.microservicio1}/entregaDevolucion/devolucion/${idTask}`, data, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        return response.data;
    } catch (error) {
        console.error('Error en Recibir Producto del Cliente:', error);
        throw error;
    }
}

export const getTaskForPhotoSesion = async () => {
    try {
        const token = Cookies.get('Token');
        const response = await axios.get(`${API_URLS.microservicio1}/fotos`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error('Error al obtener las tareas De cita primera vez:', error);
        throw error;
    }
}

export const getTasksForRoleMakeup = async () => {
    try {
        const token = Cookies.get('Token');
        const IdEmpleado = Cookies.get('userId');

        const response = await axios.get(`${API_URLS.microservicio3}/tareaMakeup/verPendientes/${IdEmpleado}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error('Error al obtener las tareas:', error);
        throw error;
    }
};

export const GetAssignentDay = async () => {
    try {
        const token = Cookies.get('Token');

        const response = await axios.get(`${API_URLS.microservicio1}/tarea`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error('Error al obtener las tareas generales :', error);
        throw error;
    }
}

export const getHistoryTransactions = async () => {
    const response = await axios.get(`${API_URLS.microservicio3}/Auditoria`);
    console.log(response.data);
    return response.data;
}

export const getSaldo = async () => {
    const response = await axios.get(`${API_URLS.microservicio3}/caja/saldo`);
    console.log(response.data);
    return response.data;
}


export const addIncomeService = async (data) => {
    const token = Cookies.get('Token');
    const response = await axios.put(`${API_URLS.microservicio3}/caja/agregar`, data, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    console.log(response)
    return response.data;
}

export const addExpenseService = async (data) => {
    const token = Cookies.get('Token');
    const response = await axios.put(`${API_URLS.microservicio3}/caja/retirar`, data, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    console.log(response)
    return response.data;
}