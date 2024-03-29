import axios from 'axios';
import API_URLS from './services';
import Cookies from 'js-cookie';

export const login = async (correo, password) => {
    const response = await axios.post(`${API_URLS.microservicio1}/login`, { correo, password });
    console.log(response);
    return response.data;
};

//Traer info de solo el usuario
export const getUserInfo = async (userId) => {
    const response = await axios.get(`${API_URLS.microservicio2}/user/${userId}`);
    return response.data;
};

//Traer info de todos los empleados

export const getWorkersId = async (idAsesor, idrol) => {
    try {
        const token = Cookies.get('Token');

        const response = await axios.get(`${API_URLS.microservicio1}/empleado`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        console.log("Datos recibidos:", response.data);

        const worker = response.data.find(worker =>
            worker.usuario._id === idAsesor && worker.usuario.rol._id === idrol);

        console.log("Worker encontrado:", worker);

        return worker ? worker.id : null;

    } catch (error) {
        console.error('Error al obtener el id del empleado:', error);
        throw error;
    }


};

export const getRol = async () => {
    const idrol = Cookies.get('idRol');
    const response = await axios.get(`${API_URLS.microservicio2}/rol/${idrol}`);
    return response.data;
};

// Traer los distintos Usuarios

