import axios from 'axios';
import API_URLS from './services';
import Cookies from 'js-cookie';
import { cookies } from 'next/dist/client/components/headers';
import { extractIdFromDBRef } from './taskService';

// Rental form service

export const getProducts = async () => {
    const responseProducts = await axios.get(`${API_URLS.microservicio1}/productos/getAll`);
    console.log(responseProducts.data);
    return responseProducts.data;
}


export const postFormulario = async (formData) => {
    const token = Cookies.get('Token');
    const response = await axios.post(`${API_URLS.microservicio1}/alquiler`, formData, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    return response.data;
};

export const postCitaMedidas = async (formData) => {
    const IdcitaMedidas = Cookies.get('IdCitaMedidas');
    const token = Cookies.get('Token');
    const response = await axios.put(`${API_URLS.microservicio1}/tarea/answer/${IdcitaMedidas}`, formData, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    return response.data;

};

export const enviarPrecios = async (datosParaEnviar, dbrefFormMedidas) => {
    try {
        const idformMedidas = extractIdFromDBRef(dbrefFormMedidas);
        const token = Cookies.get('Token');

        const response = await axios.put(`${API_URLS.microservicio3}/formMedidas/responder/${idformMedidas}`, datosParaEnviar, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        return response.data;
    } catch (error) {
        console.error('Error al enviar precios:', error);
        throw error;
    }
};

export const responderTareaModistaComplete = async (data) => {
    const idTarea = Cookies.get('IdTareaModista');
    const token = Cookies.get('Token');

    try {
        const response = await axios.put(`${API_URLS.microservicio3}/tareaModista/responder/${idTarea}`, data, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error('Error al responder a la tarea de modista:', error);
        throw error;
    }
};

export const responderTareaLavanderiaComplete = async (data) => {
    const idTarea = Cookies.get('IdTareaLavanderia');
    const token = Cookies.get('Token');

    try {
        const response = await axios.put(`${API_URLS.microservicio3}/lavanderia/answer/${idTarea}`, data, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error('Error al responder a la tarea de Lavanderia:', error);
        throw error;
    }
};

export const updateProductService = async (id, data) => {
    const token = Cookies.get('Token');

    try {
        const response = await axios.put(`${API_URLS.microservicio1}/productos/${id}`, data, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error('Error al actualizar el producto:', error);
        throw error;
    }
};

export const saveProductService = async (productData) => {
    const token = Cookies.get('Token');
    const response = await axios.post(`${API_URLS.microservicio1}/productos`, productData, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    return response.data;
}

export const deleteProductService = async (idProduct) => {
    const Token = Cookies.get('Token');
    try {
        const response = await axios.delete(`${API_URLS.microservicio1}/productos/${idProduct}`, {
            headers: {
                'Authorization': `Bearer ${Token}`
            }
        });
        console.log('Respuesta de eliminación:', response);
        return response.data;
    } catch (error) {
        console.error('Error al eliminar el Producto', error);
        throw error;
    }

}

export const postCitaPrimeraVez = async (formData) => {
    const token = Cookies.get('Token');
    const response = await axios.post(`${API_URLS.microservicio1}/cita`, formData, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    return response.data;
}

export const updateTaskStatus = async (taskId, asesorId) => {
    const updateData = {
        asesor: asesorId,
        estado: true
    };

    try {
        const token = Cookies.get('Token');
        const response = await axios.put(`${API_URLS.microservicio3}/cita/responder/${taskId}`, updateData, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        return response.data;
    } catch (error) {
        console.error('Error en updateTaskWithWorker:', error);
        throw error;
    }
}

export const updateTaskStatusPhotoSesion = async (taskId) => {
    const updateData = {
        estado: true
    };

    try {
        const token = Cookies.get('Token');
        const response = await axios.put(`${API_URLS.microservicio1}/fotos/responder/${taskId}`, updateData, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        return response.data;
    } catch (error) {
        console.error('Error en updateTaskWithWorker:', error);
        throw error;
    }
}

export const postPhotosForm = async (formData) => {
    const token = Cookies.get('Token');
    const response = await axios.post(`${API_URLS.microservicio1}/fotos`, formData, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    return response.data;
}

export const postMakeupCreate = async (formData) => {
    const token = Cookies.get('Token');
    const response = await axios.post(`${API_URLS.microservicio3}/makeup`, formData, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    return response.data;
}

export const completeMakeupTask = async (taskId) => {
    const updateData = {
        completado: true
    };

    try {
        const token = Cookies.get('Token');
        const response = await axios.put(`${API_URLS.microservicio3}/tareaMakeup/responder/${taskId}`, updateData, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        return response.data;
    } catch (error) {
        console.error('Error en updateTaskWithWorker:', error);
        throw error;
    }
}

export const enviarFechaTarea = async (taskId, fechaObjeto) => {

    try {
        const token = Cookies.get('Token');
        const response = await axios.put(`${API_URLS.microservicio3}/tarea/fecha/${taskId}`, fechaObjeto, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        return response.data;
    } catch (error) {
        console.error('Error en updateTaskWithWorker:', error);
        throw error;
    }
}