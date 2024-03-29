'use client';
import React, { useEffect, useState } from 'react';
import { Table, Select } from 'antd';
import Swal from 'sweetalert2';
import withReactContent from 'sweetalert2-react-content';
import { BreadCrumb } from 'primereact/breadcrumb';
import { MenuItem } from 'primereact/menuitem';
import { getTareasDontAsing, extractIdFromDBRef, fetchProductoName, getAllEmployees, updateTaskWithWorker, getTareasDontAsingLavanderia,updateTaskWithWorkerLavanderia } from '../../../api/taskService'; 
import './AsignentView.scss';
const MySwal = withReactContent(Swal);
const { Option } = Select;
import Cookies from 'js-cookie';
import { Button } from 'primereact/button';

interface Task {
    key: number;
    id: string;
    name: string;
    nombre: string;
    date: string;
    assignedTo: number | null;
}

interface Worker {
    id: number;
    name: string;
}

const AssignmentView = () => {
    const home: MenuItem = { icon: 'pi pi-home', url: '/' };
    const breadcrumbItems: MenuItem[] = [{ label: 'Formularios' }, { label: 'Ver y Asignar Trabajador' }];

    const [selectedOption, setSelectedOption] = useState('modista');
    const [tasks, setTasks] = useState<Task[]>([]);
    const [employees, setEmployees] = useState([]);

    useEffect(() => {
        handleOptionChange(selectedOption);
        fetchAllEmployees();
    }, [selectedOption]);

    const fetchAllEmployees = async () => {
        try {
            const allEmployees = await getAllEmployees();
            setEmployees(allEmployees);
        } catch (error) {
            console.error('Error al cargar empleados:', error);
        }
    };

    const assignTask = async (taskId: any, taskType: any) => {
        const filteredEmployees = employees.filter((employee) => employee.usuario.rol._id === rolId[taskType]);

        const employeeOptions = filteredEmployees.map((employee) => ({
            text: employee.usuario.nombreApellido,
            value: employee.id.toString()
        }));

        MySwal.fire({
            title: 'Asignar Trabajador',
            input: 'select',
            inputOptions: employeeOptions.reduce((acc, current) => {
                acc[current.value] = current.text;
                return acc;
            }, {}),
            inputPlaceholder: 'Seleccionar Trabajador',
            showCancelButton: true
        }).then(async (result) => {
            if (result.isConfirmed) {
                try {
                    if (taskType === 'modista') {
                        await updateTaskWithWorker(taskId, { [taskType]: result.value });
                    } else if (taskType === 'lavanderia') {
                        await updateTaskWithWorkerLavanderia(taskId, { [taskType]: result.value });
                    }
    
                    console.log(`Tarea ${taskId} asignada a trabajador ${result.value}`);
                    handleOptionChange(selectedOption);
                    Swal.fire({
                        title: 'Asignación completada',
                        text: 'El trabajador ha sido asignado a la tarea exitosamente',
                        icon: 'success',
                        confirmButtonText: 'Ok'
                    });
                } catch (error) {
                    console.error('Error al asignar el trabajador:', error);
                }
            }
        });
    };

    const handleOptionChange = async (value: any) => {
        setSelectedOption(value);
        if (value === 'modista') {
            try {
                const modistaTasks = await getTareasDontAsing();

                const tasksWithProduct = await Promise.all(
                    modistaTasks.map(async (task) => {
                        const productId = task.producto;
                        let productName = 'Producto no encontrado';

                        if (productId) {
                            try {
                                const product = await fetchProductoName(productId);
                                productName = product.nombre;
                            } catch (error) {
                                console.error('Error al cargar el producto:', error);
                            }
                        }

                        return {
                            key: task._id,
                            id: task._id,
                            name: 'Tarea Modista',
                            nombre: productName,
                            date: task.fecha,
                            assignedTo: null
                        };
                    })
                );

                setTasks(tasksWithProduct);
            } catch (error) {
                console.error('Error al cargar las tareas de modista:', error);
            }
        } else if (value === 'lavanderia') {
            try {
                const lavanderiaTask = await getTareasDontAsingLavanderia();

                const tasksWithProduct = await Promise.all(
                    lavanderiaTask.map(async (task) => {
                        const productId = task.producto;
                        let productName = 'Producto no encontrado';

                        if (productId) {
                            try {
                                const product = await fetchProductoName(productId);
                                productName = product.nombre;
                            } catch (error) {
                                console.error('Error al cargar el producto:', error);
                            }
                        }

                        return {
                            key: task._id,
                            id: task._id,
                            name: 'Tarea Lavanderia',
                            nombre: productName,
                            date: task.fecha,
                            assignedTo: null
                        };
                    })
                );

                setTasks(tasksWithProduct);
            } catch (error) {
                console.error('Error al cargar las tareas de lavanderia:', error);
            }
        }
    };

    const rolId = {
        modista: '64a780574f5c1f4272d8e66c',
        lavanderia: '64c99d28bf3ae63b80f936e3',
        maquilladora: '653ea80670556042587486bd'
    };

    const columnModista = [
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
            title: 'Nombre Producto',
            dataIndex: 'nombre',
            key: 'nombre'
        },
        {
            title: 'Fecha Que se debe entregar',
            dataIndex: 'date',
            key: 'date'
        },
        {
            title: 'Asignar',
            key: 'assign',
            render: (_, record: any) => <Button onClick={() => assignTask(record.id, 'modista')}>Asignar Modista</Button>
        }
    ];

    // Columnas para Lavandería
    const columnLavanderia = [
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
            title: 'Nombre Producto',
            dataIndex: 'nombre',
            key: 'nombre'
        },
        {
            title: 'Fecha a Entregar',
            dataIndex: 'date',
            key: 'date'
        },
        {
            title: 'Asignar',
            key: 'assign',
            render: (_, record: any) => <Button onClick={() => assignTask(record.id, 'lavanderia')}>Asignar Lavanderia</Button>
        }
    ];

    // // Columnas para Maquilladora
    // const columnMaquilladora = [
    //     {
    //         title: 'ID',
    //         dataIndex: 'id',
    //         key: 'id'
    //     },
    //     {
    //         title: 'Nombre',
    //         dataIndex: 'name',
    //         key: 'name'
    //     },
    //     {
    //         title: 'Descripción',
    //         dataIndex: 'description',
    //         key: 'description'
    //     },
    //     {
    //         title: 'Fecha',
    //         dataIndex: 'date',
    //         key: 'date'
    //     },
    //     {
    //         title: 'Asignar',
    //         key: 'assign',
    //         render: (_, record: any) => <Button onClick={() => assignTask(record.id, 'lavanderia')}>Asignar Maquilladora</Button>
    //     }
    // ];

    const getCurrentColumns = () => {
        switch (selectedOption) {
            case 'modista':
                return columnModista;
            case 'lavanderia':
                return columnLavanderia;
            // case 'maquilladora':
            //     return columnMaquilladora;
            default:
                return columnModista;
        }
    };

    return (
        <div className="containerFormTask">
            <div className="col-12 ">
                <div className="card">
                    <h5>Asignar Trabajador</h5>
                    <BreadCrumb home={home} model={breadcrumbItems} />
                </div>
            </div>
            <div className="col-12">
                <div className="card">
                    <div className="buttonContainer">
                        <h5>Lista de Tareas</h5>
                        {/* Dropdown para seleccionar la opción */}
                        <Select defaultValue="modista" style={{ width: 120, marginBottom: 10 }} onChange={handleOptionChange}>
                            <Option value="modista">Asignar Modista</Option>
                            <Option value="lavanderia">Asignar Lavandería</Option>
                            {/* <Option value="maquilladora">Asignar Maquilladora</Option> */}
                        </Select>{' '}
                    </div>
                    <div className="table-responsive-container">

                    <Table columns={getCurrentColumns()} dataSource={tasks} scroll={{ x: 1300 }} />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default AssignmentView;
