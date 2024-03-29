// Importaciones necesarias
'use client';
import React, { useEffect, useState } from 'react';
import Swal from 'sweetalert2';
import { Table } from 'antd';
import withReactContent from 'sweetalert2-react-content';
import { BreadCrumb } from 'primereact/breadcrumb';
import { MenuItem } from 'primereact/menuitem';
import { Button } from 'primereact/button';
import './taskview.scss';
import Item from 'antd/es/list/Item';
import { getTaskForPhotoSesion } from '../../../api/taskService';
import { updateTaskStatusPhotoSesion } from '../../../api/formServices';
import { getRol } from '../../../api/authServices';
import Cookies from 'js-cookie';

const MySwal = withReactContent(Swal);

// export const config = { runtime: 'client' };

const PhotosResponse = () => {
    const [tasks, setTasks] = useState([]);
    const [role, setRole] = useState('');
    const home: MenuItem = { icon: 'pi pi-home', url: '/' };
    const breadcrumbItems: MenuItem[] = [{ label: 'Formularios' }, { label: 'Ver Sesiones de Fotos' }];
    //Funciones Para Rol Asesor

    useEffect(() => {
        const fetchRoleAndTasks = async () => {
            try {
                const rolData = await getRol();
                setRole(rolData.name);

                let tasksData = [];
                if (rolData.name === 'Asesor' || rolData.name === 'Admin') {
                    tasksData = await fetchAndFormatTasksForAsesor();
                }

                setTasks(tasksData);
            } catch (error) {
                console.error('Error:', error);
            }
        };

        fetchRoleAndTasks();
    }, []);

    const loadTasks = async () => {
        try {
            const rolData = await getRol();
            setRole(rolData.name);

            let tasksData = [];
            if (rolData.name === 'Asesor' || rolData.name === 'Admin') {
                tasksData = await fetchAndFormatTasksForAsesor();
            }

            setTasks(tasksData);
        } catch (error) {
            console.error('Error:', error);
        }
    };

    // Llama a loadTasks cuando el componente se monta
    useEffect(() => {
        loadTasks();
    }, []);

    const handleUpdateTaskStatus = (taskId) => {
        updateTaskStatusPhotoSesion(taskId)
            .then(() => {
                Swal.fire('Éxito', 'La cita ha sido actualizada correctamente', 'success');
                loadTasks();
            })
            .catch((error) => {
                console.error('Error al actualizar la cita:', error);
                Swal.fire('Error', 'Hubo un problema al actualizar la cita', 'error');
            });
    };
    // Función para obtener y formatear las tareas para el Asesor
    const fetchAndFormatTasksForAsesor = async () => {
        const rawTasks = await getTaskForPhotoSesion();
        const tasksWithAdditionalInfo = await Promise.all(
            rawTasks.map(async (task: any) => {
                return {
                    ...task,
                    asesor: rawTasks.asesor
                };
            })
        );

        return tasksWithAdditionalInfo;
    };
    const getColumnsBasedOnRole = (role: any) => {
        switch (role) {
            case 'Asesor':
                return getColumnsForAsesor();
            case 'Modisteria':
                return getColumnsForAsesor();

            case 'Admin':
                return getColumnsForAsesor();
            default:
                return [];
        }
    };

    function formatFechaGMT(fecha) {
        const dateObj = new Date(fecha);

        const options: any = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit', timeZone: 'GMT' };

        let formattedDate = new Intl.DateTimeFormat('es-ES', options).format(dateObj);

        return formattedDate;
    }

    // Función para definir las columnas para el Asesor
    const getColumnsForAsesor = () => {
        return [
            {
                title: 'ID Tarea',
                dataIndex: '_id',
                key: '_id'
            },
            {
                title: 'Fecha de Sesion Fotos',
                dataIndex: 'fecha',
                key: 'fecha',
                render: (fecha) => <span>{formatFechaGMT(fecha)}</span>
            },
            {
                title: 'Nombre cliente ',
                dataIndex: 'nombreCliente',
                key: 'nombreCliente'
            },
            {
                title: 'Teléfono',
                dataIndex: 'numeroCliente',
                key: 'telefono'
            },
            {
                title: 'Acciones',
                key: 'acciones',
                render: (text, record) => (
                    <Button
                        disabled={record.estado}
                        onClick={() => {
                            if (!record.estado) {
                                MySwal.fire({
                                    title: '¿Completaste esta Sesion de Fotos?',
                                    showCancelButton: true,
                                    confirmButtonText: 'Sí',
                                    cancelButtonText: 'No'
                                }).then((result) => {
                                    if (result.isConfirmed) {
                                        handleUpdateTaskStatus(record._id);
                                    }
                                });
                            }
                        }}
                    >
                        {record.estado ? 'Sesion de Fotos hecha' : 'Responder Sesion de Fotos'}
                    </Button>
                )
            }
        ];
    };

    return (
        <div className="containerFormTask">
            <div className="col-12 ">
                <div className="card">
                    <h5>Ver Tareas y Actividades</h5>
                    <BreadCrumb home={home} model={breadcrumbItems} />
                </div>
            </div>
            <div className="col-12 ">
                <div className="card">
                    <div className="buttonContainer">
                        <h5>Lista de Sesiones de Fotos</h5>
                        {/*<Button className="mb-2" onClick={showNewTaskModal} label="Crear Nueva Tarea" />*/}
                    </div>
                    <div className="table-responsive-container">
                        <Table columns={getColumnsBasedOnRole(role)} dataSource={tasks} scroll={{ x: 1300 }} />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default PhotosResponse;
