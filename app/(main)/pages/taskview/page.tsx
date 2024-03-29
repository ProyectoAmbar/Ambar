'use client';
import React, { useEffect, useState } from 'react';
import Swal from 'sweetalert2';
import { Table } from 'antd';
import withReactContent from 'sweetalert2-react-content';
import { BreadCrumb } from 'primereact/breadcrumb';
import { MenuItem } from 'primereact/menuitem';
import { Button } from 'primereact/button';
import { AllGeneralTask } from '../../../api/taskService';
import './taskview.scss';
import Item from 'antd/es/list/Item';

const MySwal = withReactContent(Swal);

// export const config = { runtime: 'client' };

interface TaskType {
    key: number;
    id: string;
    name: string;
    description: string;
    // type: string;
}

const columns = [
    {
        title: 'ID',
        dataIndex: 'id',
        key: 'id'
    },
    {
        title: 'Nombre',
        dataIndex: 'name',
        key: 'name'
    },
    {
        title: 'Descripción',
        dataIndex: 'description',
        key: 'description'
    }
    /* {
        title: 'Tipo',
        dataIndex: 'type',
        key: 'type'
    }*/
];

const TaskView = () => {
    const [tasks, setTasks] = useState<TaskType[]>([]);

    const home: MenuItem = { icon: 'pi pi-home', url: '/' };
    const breadcrumbItems: MenuItem[] = [{ label: 'Formularios' }, { label: 'Ver y Crear Tareas' }];

    useEffect(() => {
        const fetchTasks = async () => {
            try {
                const data = await AllGeneralTask();
                console.log('informacion', data);
                const formattedTasks = data.map((item: any, index: number) => ({
                    key: index,
                    id: item._id,
                    name: item.formulario,
                    description: item.producto
                    //type: item.type
                }));
                setTasks(formattedTasks);
            } catch (error) {
                console.error('Error al cargar las tareas:', error);
            }
        };

        fetchTasks();
    }, []);

    const showNewTaskModal = () => {
        MySwal.fire({
            title: 'Selecciona la nueva tarea',
            showCancelButton: true,
            cancelButtonText: 'Cancelar',
            html: `
                <button id="alquiler" class="swal2-confirm swal2-styled" style="border-left-color: #3085d6; border-right-color: #3085d6">Nuevo Alquiler</button>
                <button id="maquillaje" class="swal2-deny swal2-styled" style="display: inline-block;">Nuevo Maquillaje</button>
                <button id="sesionFotos" class="swal2-confirm swal2-styled" style="margin-left: 8px;">Nueva Sesión de Fotos</button>
                <button id="primeravez" class="swal2-confirm swal2-styled" style="margin-left: 8px;">Nueva cita Primera Vez</button>
            `,
            focusConfirm: false,
            showConfirmButton: false,
            didOpen: () => {
                document.getElementById('alquiler').addEventListener('click', () => {
                    window.location.href = '/pages/formsAlquiler';
                });
    
                document.getElementById('maquillaje').addEventListener('click', () => {
                    window.location.href = '/pages/formsMakeup';
                });
    
                document.getElementById('sesionFotos').addEventListener('click', () => {
                    window.location.href = '/pages/FormPhoto';
                });
                document.getElementById('primeravez').addEventListener('click', () => {
                    window.location.href = '/pages/formsCitaPrimera';
                });
            }
        });
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
                        <Button className="mb-2" onClick={showNewTaskModal} label="Crear Nueva Tarea" />
                    </div>
                    <div className="table-responsive-container">
                        <Table columns={columns} dataSource={tasks.map((task) => ({ ...task, key: task.id }))} scroll={{ x: 1300 }} />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default TaskView;
