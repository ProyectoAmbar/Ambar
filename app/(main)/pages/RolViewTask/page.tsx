// Importaciones necesarias
'use client';
import React, { useEffect, useState } from 'react';
import Swal from 'sweetalert2';
import { Table } from '../../../../node_modules/antd/es/index';
import withReactContent from 'sweetalert2-react-content';
import { BreadCrumb } from 'primereact/breadcrumb';
import { MenuItem } from 'primereact/menuitem';
import { Button } from 'primereact/button';
import { extractIdFromDBRef } from '../../../api/taskService';

import './taskview.scss';
import Item from 'antd/es/list/Item';
import {
    getTasksForRoleAsesor,
    fetchAsesorName,
    fetchProductoName,
    getTasksForRoleModista,
    fetchModistaName,
    fetchLavanderiaName,
    getTasksForRoleLavanderia,
    getTasksForRoleMakeup,
    fetchmakeupbyUserid,
    fetchProductoName2,
    GetAssignentDay
} from '../../../api/taskService';
import { completeMakeupTask, enviarFechaTarea } from '../../../api/formServices';
import { getRol } from '../../../api/authServices';
import Cookies from 'js-cookie';
import { DataTable } from 'primereact/datatable';

const MySwal = withReactContent(Swal);

// export const config = { runtime: 'client' };

const RolViewTask = () => {
    const [tasks, setTasks] = useState([]);
    const [role, setRole] = useState('');
    const home: MenuItem = { icon: 'pi pi-home', url: '/' };
    const breadcrumbItems: MenuItem[] = [{ label: 'Formularios' }, { label: 'Ver y mis Tareas' }];

    const handleTaskClick = (taskId: any) => {
        window.location.href = `/pages/formsMedidas`;
        Cookies.set('IdCitaMedidas', taskId);
    };

    const handleTaskClickModista = (taskId: any) => {
        window.location.href = `/pages/formsSastreria`;
        Cookies.set('IdTareaModista', taskId);
    };

    const handleTaskClickLavanderia = (taskId: any) => {
        window.location.href = `/pages/formsLavanderia`;
        Cookies.set('IdTareaLavanderia', taskId);
    };
    const handleTaskClickMakeup = async (taskId) => {
        const result = await Swal.fire({
            title: '¿Confirmas que el maquillaje ha sido completado?',
            text: 'Esta acción no se puede deshacer',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Sí, completar',
            cancelButtonText: 'Cancelar'
        });

        if (result.isConfirmed) {
            try {
                await completeMakeupTask(taskId);
                Swal.fire('Completado!', 'El maquillaje ha sido completado exitosamente.', 'success');
            } catch (error) {
                Swal.fire('Error', 'No se pudo completar el maquillaje. Por favor, intenta de nuevo.', 'error');
            }
        }
    };

    //Funciones Para Rol Asesor

    // Función para obtener y formatear las tareas para el Asesor
    const fetchAndFormatTasksForAsesor = async () => {
        const asesorId = Cookies.get('idEmpleado');
        console.log('ID del asesor de las cookies:', asesorId);
        const rawTasks = await getTasksForRoleAsesor();
        const additionalTasks = await GetAssignentDay();

        console.log('Tareas adicionales antes del filtrado:', additionalTasks);

        const filteredAdditionalTasks = additionalTasks.filter((task) => {
            const asesorIdFromTask = extractIdFromDBRef(task.asesor);
            console.log('ID del asesor de la tarea:', asesorIdFromTask);
            const passesFilter = !task.fechaCitaDeMedidas && asesorIdFromTask === asesorId;
            console.log('Pasa el filtro:', passesFilter);
            return passesFilter;
        });

        console.log('Tareas adicionales después del filtrado:', filteredAdditionalTasks);

        const allTasks = [...rawTasks.map((task) => ({ ...task, origin: 'common' })), ...filteredAdditionalTasks.map((task) => ({ ...task, origin: 'additional' }))];

        const tasksWithAdditionalInfo = await Promise.all(
            allTasks.map(async (task) => {
                const asesorIdFromTask = task.asesor;
                const asesorInfo = await fetchAsesorName(asesorIdFromTask);
                const productoInfo = await fetchProductoName(task.producto);

                return {
                    ...task,
                    asesor: asesorInfo.usuario.nombreApellido,
                    producto: productoInfo.nombre
                };
            })
        );

        return tasksWithAdditionalInfo;
    };

    const handleAdditionalTaskClick = async (taskId) => {
        MySwal.fire({
            title: 'Elegir Fecha',
            html: `<input type="date" id="fecha" class="swal2-input">`,
            confirmButtonText: 'Guardar',
            showCancelButton: true,
            preConfirm: () => {
                const fechaInput = Swal.getPopup().querySelector('#fecha') as HTMLInputElement;
                if (!fechaInput || !fechaInput.value) {
                    Swal.showValidationMessage(`Por favor elige una fecha`);
                    return false;
                }
                return fechaInput.value;
            }
        }).then(async (result) => {
            if (result.isConfirmed && result.value) {
                const [año, mes, dia] = result.value.split('-').map((num) => parseInt(num, 10));
                const fechaObjeto = { dia, mes, año };

                try {
                    await enviarFechaTarea(taskId, fechaObjeto);
                    console.log('Fecha enviada con éxito');
                    await Swal.fire('¡Éxito!', 'La fecha ha sido guardada.', 'success');

                    const updatedTasks = await fetchAndFormatTasksForAsesor();
                    setTasks(updatedTasks);
                } catch (error) {
                    console.error('Error al enviar la fecha', error);
                    Swal.fire('Error', 'Hubo un problema al guardar la fecha.', 'error');
                }
            }
        });
    };

    const fetchAndFormatTasksForModista = async () => {
        const rawTasks = await getTasksForRoleModista();
        const tasksWithAdditionalInfo = await Promise.all(
            rawTasks.map(async (task: any) => {
                const ModistaInfo = await fetchModistaName(task.modista);
                const productoInfo = await fetchProductoName(task.producto);

                return {
                    ...task,
                    modista: ModistaInfo.usuario.nombreApellido,
                    producto: productoInfo.nombre
                };
            })
        );

        return tasksWithAdditionalInfo;
    };

    const fetchAndFormatTasksForLavanderia = async () => {
        const rawTasks = await getTasksForRoleLavanderia();
        const tasksWithAdditionalInfo = await Promise.all(
            rawTasks.map(async (task: any) => {
                const LavanderiaInfo = await fetchLavanderiaName(task.lavanderia);
                const productoInfo = await fetchProductoName(task.producto);

                return {
                    ...task,
                    lavanderia: LavanderiaInfo.usuario.nombreApellido,
                    producto: productoInfo.nombre
                };
            })
        );

        return tasksWithAdditionalInfo;
    };

    function formatFechaGMT(fecha) {
        const dateObj = new Date(fecha);

        const options: any = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit', timeZone: 'GMT' };

        let formattedDate = new Intl.DateTimeFormat('es-ES', options).format(dateObj);

        return formattedDate;
    }

    const fetchAndFormatTasksForMakeup = async () => {
        const rawTasks = await getTasksForRoleMakeup();
        const tasksWithAdditionalInfo = await Promise.all(
            rawTasks.map(async (task: any) => {
                const makeupInfo = await fetchmakeupbyUserid(task.idMakeup);
                const productoInfo = await fetchProductoName2(task.referencia);

                return {
                    ...task,
                    maquilladora: makeupInfo.usuario.nombreApellido,
                    producto: productoInfo.nombre
                };
            })
        );

        return tasksWithAdditionalInfo;
    };

    //Fin Funciones Rol Asesor

    useEffect(() => {
        const fetchRoleAndTasks = async () => {
            try {
                const rolData = await getRol();
                setRole(rolData.name);

                let tasksData = [];
                if (rolData.name === 'Asesor') {
                    tasksData = await fetchAndFormatTasksForAsesor();
                } else if (rolData.name === 'Modisteria') {
                    tasksData = await fetchAndFormatTasksForModista();
                } else if (rolData.name === 'lavanderia') {
                    tasksData = await fetchAndFormatTasksForLavanderia();
                } else if (rolData.name === 'Makeup') {
                    tasksData = await fetchAndFormatTasksForMakeup();
                }

                setTasks(tasksData);
            } catch (error) {
                console.error('Error:', error);
            }
        };

        fetchRoleAndTasks();
    }, []);

    const getColumnsBasedOnRole = (role: any) => {
        switch (role) {
            case 'Asesor':
                return getColumnsForAsesor();
            case 'Modisteria':
                return getColumnsForModista();

            case 'lavanderia':
                return getColumnsForLavanderia();
            case 'Makeup':
                return getColumnsForMaquilladora();
            default:
                return [];
        }
    };

    // Función para definir las columnas para el Asesor
    const getColumnsForAsesor = () => {
        return [
            {
                title: 'ID Tarea',
                dataIndex: '_id',
                key: '_id'
            },
            {
                title: 'Nombre Asesor',
                dataIndex: 'asesor',
                key: 'asesor'
            },
            {
                title: 'Fecha de Cita',
                dataIndex: 'fechaCitaDeMedidas',
                key: 'fechaCitaDeMedidas'
            },
            {
                title: 'Necesita Modista',
                dataIndex: 'necesitaModista',
                key: 'necesitaModista',
                render: (necesitaModista: any) => (necesitaModista ? 'Sí' : 'No')
            },
            {
                title: 'Producto',
                dataIndex: 'producto',
                key: 'producto'
            },
            {
                title: 'Acciones',
                key: 'acciones',
                render: (text, record) => {
                    if (record.origin === 'common') {
                        return (
                            <Button disabled={record.estado} onClick={() => handleTaskClick(record._id)}>
                                {record.estado ? 'Cita Realizada' : 'Hacer Cita Medidas'}
                            </Button>
                        );
                    } else if (record.origin === 'additional') {
                        return <Button onClick={() => handleAdditionalTaskClick(record._id)}>{'Elegir Fecha'}</Button>;
                    }
                }
            }
        ];
    };

    const getColumnsForModista = () => {
        return [
            {
                title: 'ID Tarea',
                dataIndex: '_id',
                key: '_id'
            },
            {
                title: 'Nombre Modista',
                dataIndex: 'modista',
                key: 'modista'
            },
            {
                title: 'Fecha de Arreglos a entregar',
                dataIndex: 'fecha',
                key: 'fechaCitaDeMedidas'
            },
            // {
            //     title: 'Fecha de Arreglos a entregar',
            //     dataIndex: 'fecha',
            //     key: 'fecha',
            //     render: (necesitaModista: any) => (necesitaModista ? 'Sí' : 'No')
            // },
            {
                title: 'Producto',
                dataIndex: 'producto',
                key: 'producto'
            },
            {
                title: 'Acciones',
                key: 'acciones',
                render: (text, record: any) => (
                    <Button disabled={record.estado} onClick={() => handleTaskClickModista(record._id)}>
                        {record.estado ? 'Producto Arreglado' : 'Arreglar Producto'}
                    </Button>
                )
            }
        ];
    };

    const getColumnsForLavanderia = () => {
        return [
            {
                title: 'ID Tarea',
                dataIndex: '_id',
                key: '_id'
            },
            {
                title: 'Nombre Lavandera',
                dataIndex: 'lavanderia',
                key: 'lavanderia'
            },
            {
                title: 'Fecha de Lavado para entregar',
                dataIndex: 'fecha',
                key: 'fechaCitaDeMedidas'
            },
            // {
            //     title: 'Fecha de Arreglos a entregar',
            //     dataIndex: 'fecha',
            //     key: 'fecha',
            //     render: (necesitaModista: any) => (necesitaModista ? 'Sí' : 'No')
            // },
            {
                title: 'Producto',
                dataIndex: 'producto',
                key: 'producto'
            },
            {
                title: 'Acciones',
                key: 'acciones',
                render: (text, record: any) => (
                    <Button disabled={record.estado} onClick={() => handleTaskClickLavanderia(record._id)}>
                        {record.estado ? 'Producto Lavado' : 'Lavar Producto'}
                    </Button>
                )
            }
        ];
    };

    const getColumnsForMaquilladora = () => {
        return [
            {
                title: 'ID Tarea',
                dataIndex: '_id',
                key: '_id'
            },
            {
                title: 'Nombre Maquilladora',
                dataIndex: 'maquilladora',
                key: 'maquilladora'
            },
            {
                title: 'Fecha de Cita',
                dataIndex: 'fecha',
                key: 'fecha',
                render: (fecha) => <span>{formatFechaGMT(fecha)}</span>
            },
            // {
            //     title: 'Fecha de Arreglos a entregar',
            //     dataIndex: 'fecha',
            //     key: 'fecha',
            //     render: (necesitaModista: any) => (necesitaModista ? 'Sí' : 'No')
            // },
            {
                title: 'Producto',
                dataIndex: 'producto',
                key: 'producto'
            },
            {
                title: 'Acciones',
                key: 'acciones',
                render: (text, record: any) => (
                    <Button disabled={record.completado} onClick={() => handleTaskClickMakeup(record._id)}>
                        {record.completado ? 'Makeup Completado' : 'Completar'}
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
                        <h5>Lista de Tareas</h5>
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

export default RolViewTask;
