// Importaciones necesarias
'use client';
import React, { useEffect, useState } from 'react';
import Swal from 'sweetalert2';
import withReactContent from 'sweetalert2-react-content';
import { BreadCrumb } from 'primereact/breadcrumb';
import { MenuItem } from 'primereact/menuitem';
import { Button } from 'primereact/button';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import './taskview.scss';
import { getTasksForRoleAsesorCita } from '../../../api/taskService';
import { updateTaskStatus } from '../../../api/formServices';
import { getRol } from '../../../api/authServices';
import Cookies from 'js-cookie';

const MySwal = withReactContent(Swal);

const CitaPrimeraRespond = () => {
    const [tasks, setTasks] = useState([]);
    const [role, setRole] = useState('');
    const home = { icon: 'pi pi-home', url: '/' };
    const breadcrumbItems = [{ label: 'Formularios' }, { label: 'Ver Citas Primera Vez' }];

    useEffect(() => {
        loadTasks();
        // eslint-disable-next-line
    }, []);

    useEffect(() => {
        const fetchRoleAndTasks = async () => {
            const rolData = await getRol();
            setRole(rolData.name);
            const tasksData = await fetchAndFormatTasksForAsesor(rolData.name);
            setTasks(tasksData);
        };

        fetchRoleAndTasks();
        // eslint-disable-next-line
    }, []);

    const loadTasks = async () => {
        const rolData = await getRol();
        setRole(rolData.name);
        const tasksData = await fetchAndFormatTasksForAsesor(rolData.name);
        setTasks(tasksData);
    };

    const handleUpdateTaskStatus = async (taskId) => {
        const asesorId = Cookies.get('idEmpleado');
        try {
            await updateTaskStatus(taskId, asesorId);
            Swal.fire('Éxito', 'La cita ha sido actualizada correctamente', 'success');
            await loadTasks();
        } catch (error) {
            console.error('Error al actualizar la cita:', error);
            Swal.fire('Error', 'Hubo un problema al actualizar la cita', 'error');
        }
    };

    const fetchAndFormatTasksForAsesor = async (rol) => {
        if (rol === 'Asesor' || rol === 'Admin') {
            const rawTasks = await getTasksForRoleAsesorCita();
            return rawTasks.map((task) => ({
                ...task,
                asesor: task.asesor
            }));
        }
        return [];
    };

    const formatFechaGMT = (fecha) => {
        const dateObj = new Date(fecha);
        const options: any = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit', timeZone: 'GMT' };
        return new Intl.DateTimeFormat('es-ES', options).format(dateObj);
    };

    const dateBodyTemplate = (rowData) => {
        return formatFechaGMT(rowData.fecha);
    };

    const actionBodyTemplate = (rowData) => {
        return <Button label={rowData.estado ? 'Cita Respondida' : 'Responder Cita'} className="p-button-raised p-button-success" disabled={rowData.estado} onClick={() => confirmUpdate(rowData)} />;
    };

    const confirmUpdate = (rowData) => {
        MySwal.fire({
            title: '¿Completaste esta cita de primera vez?',
            showCancelButton: true,
            confirmButtonText: 'Sí',
            cancelButtonText: 'No'
        }).then((result) => {
            if (result.isConfirmed) {
                handleUpdateTaskStatus(rowData._id);
            }
        });
    };

    const columns = [
        { field: '_id', header: 'ID Tarea' },
        { field: 'fecha', header: 'Fecha de Cita', body: dateBodyTemplate },
        { field: 'motivo', header: 'Motivo' },
        { field: 'nombreCliente', header: 'Nombre Cliente' },
        { field: 'apellidoCliente', header: 'Apellido Cliente' },
        { field: 'telefono', header: 'Teléfono' },
        { field: 'acciones', header: 'Acciones', body: actionBodyTemplate }
    ];

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
                        <h5>Lista de Citas Primera vez</h5>
                    </div>
                    <div className="table-responsive-container">
                        <DataTable value={tasks} scrollable scrollHeight="flex">
                            {columns.map((col, i) => (
                                <Column key={i} field={col.field} header={col.header} body={col.body} />
                            ))}
                        </DataTable>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default CitaPrimeraRespond;
