'use client';
import React, { useEffect, useState } from 'react';
import Swal from 'sweetalert2';
import withReactContent from 'sweetalert2-react-content';
import { BreadCrumb } from 'primereact/breadcrumb';
import { MenuItem } from 'primereact/menuitem';
import { Dropdown } from 'primereact/dropdown';
import { Button } from 'primereact/button';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Dialog } from 'primereact/dialog';
import { Calendar } from 'primereact/calendar';
import './AsignentView.scss';
import { getTareasDontAsing, extractIdFromDBRef, fetchProductoName, getAllEmployees, updateTaskWithWorker, getAllDeliver, getAllReturns, updateTaskResponse, updateResponseReturn } from '../../../api/taskService';

const MySwal = withReactContent(Swal);

interface Task {
    key: string;
    id: string;
    name: string;
    nombre: string;
    date: string;
}

const Deliver = () => {
    const home: MenuItem = { icon: 'pi pi-home', url: '/' };
    const breadcrumbItems: MenuItem[] = [{ label: 'Formularios' }, { label: 'Ver y Responder' }];

    const [selectedOption, setSelectedOption] = useState('deliver');
    const [tasks, setTasks] = useState<Task[]>([]);
    const [employees, setEmployees] = useState([]);
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [devolutionDate, setDevolutionDate] = useState('');
    const [selectedTaskId, setSelectedTaskId] = useState(null);
    const [selectedTaskDeliveryDate, setSelectedTaskDeliveryDate] = useState(null);

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

    const openResponseModal = (taskId, deliveryDate) => {
        setSelectedTaskId(taskId);
        setSelectedTaskDeliveryDate(deliveryDate);
        setIsModalVisible(true);
    };

    const responseTask = async (taskId: any, taskType: any) => {};

    const handleOptionChange = async (value: any) => {
        setSelectedOption(value);
        if (value === 'deliver') {
            try {
                const deliverTask = await getAllDeliver();
                const tasksWithProduct = await Promise.all(
                    deliverTask.map(async (task) => {
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
                            name: 'Entregar Producto',
                            nombre: productName,
                            date: task.fechaEntrega,
                            assignedTo: null
                        };
                    })
                );

                setTasks(tasksWithProduct);
            } catch (error) {
                console.error('Error al cargar las tareas de modista:', error);
            }
        } else if (value === 'returns') {
            try {
                const returnsTask = await getAllReturns();

                const tasksWithProduct = await Promise.all(
                    returnsTask.map(async (task) => {
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
                            name: 'Recibir Producto',
                            nombre: productName,
                            date: task.fechaDevolucion,
                            assignedTo: null
                        };
                    })
                );

                setTasks(tasksWithProduct);
            } catch (error) {
                console.error('Error al Recibir el Producto:', error);
            }
        }
    };

    const rolId = {
        modista: '64a780574f5c1f4272d8e66c',
        lavanderia: '64c99d28bf3ae63b80f936e3',
        maquilladora: '653ea80670556042587486bd'
    };

    const deliverColumnTemplate = (rowData: Task) => {
        return <Button label="Entregar A cliente" onClick={() => openResponseModal(rowData.id, rowData.date)} />;
    };

    const returnsColumnTemplate = (rowData: Task) => {
        return <Button label="Recibir Producto" onClick={() => acceptReturn(rowData.id)} />;
    };

    const dateTemplate = (rowData: Task) => {
        return <span>{new Date(rowData.date).toLocaleDateString()}</span>;
    };

    const renderFooter = () => {
        return (
            <div>
                <Button label="Cancelar" icon="pi pi-times" onClick={() => setIsModalVisible(false)} className="p-button-text" />
                <Button label="Enviar" icon="pi pi-check" onClick={submitResponse} autoFocus />
            </div>
        );
    };

    const submitResponse = async () => {
        if (!devolutionDate) {
            Swal.fire({
                title: 'Error',
                text: 'Por favor, seleccione una fecha de devolución.',
                icon: 'error'
            });
            return;
        }

        const selectedDate = new Date(devolutionDate);
        const deliveryDate = new Date(selectedTaskDeliveryDate);
        const maxReturnDate = new Date(deliveryDate);
        maxReturnDate.setDate(maxReturnDate.getDate() + 8);

        if (selectedDate > maxReturnDate) {
            Swal.fire({
                title: 'Fecha no permitida',
                text: 'La fecha de devolución debe ser máximo 8 días después de la fecha de entrega.',
                icon: 'error'
            });
            return;
        }

        const formattedDate = selectedDate.toISOString().split('T')[0];
        const payload = {
            entregaCompletado: true,
            fechaDevolucion: formattedDate
        };

        try {
            await updateTaskResponse(selectedTaskId, payload);
            handleOptionChange(selectedOption);
            Swal.fire({
                title: 'Éxito',
                text: 'La respuesta ha sido enviada correctamente.',
                icon: 'success'
            });
        } catch (error) {
            Swal.fire({
                title: 'Error',
                text: 'Hubo un error al enviar la respuesta.',
                icon: 'error'
            });
            console.error('Error al enviar la respuesta:', error);
        }
    };

    const acceptReturn = async (taskId) => {
        const result = await Swal.fire({
            title: '¿Aceptar el producto?',
            text: 'Confirma si has recibido el producto.',
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Sí, aceptar',
            cancelButtonText: 'No'
        });

        if (result.isConfirmed) {
            const payload = {
                devolucionCompletado: true
            };

            try {
                await updateResponseReturn(taskId, payload);
                handleOptionChange(selectedOption);
                Swal.fire('Aceptado', 'El producto ha sido aceptado exitosamente.', 'success');
            } catch (error) {
                Swal.fire('Error', 'Hubo un problema al aceptar el producto.', 'error');
                console.error('Error al aceptar el producto:', error);
            }
        }
    };

    const optionItems = [
        { label: 'Ver Entregas', value: 'deliver' },
        { label: 'Ver Devoluciones', value: 'returns' }
    ];

    return (
        <div className="containerFormTask">
            <div className="col-12 ">
                <div className="card">
                    <h5>Ver Entregas O Devoluciones</h5>
                    <BreadCrumb home={home} model={breadcrumbItems} />
                </div>
            </div>
            <div className="col-12">
                <div className="card">
                    <div className="buttonContainer">
                        <h5>Lista de Entregas O Devoluciones</h5>
                        <Dropdown value={selectedOption} options={optionItems} onChange={(e) => handleOptionChange(e.value)} placeholder="Seleccionar Opción" />
                    </div>
                    <div className="table-responsive-container">
                        <DataTable value={tasks} responsiveLayout="scroll">
                            <Column field="id" header="ID" />
                            <Column field="name" header="Nombre" />
                            <Column field="nombre" header="Nombre Producto" />
                            <Column field="date" header="Fecha" body={dateTemplate} />
                            <Column body={selectedOption === 'deliver' ? deliverColumnTemplate : returnsColumnTemplate} />
                        </DataTable>
                    </div>
                </div>
            </div>
            <Dialog header="Respuesta de Entrega Producto" visible={isModalVisible} style={{ width: '50vw' }} footer={renderFooter} onHide={() => setIsModalVisible(false)}>
                <div className="p-field">
                    <label htmlFor="date">Fecha de Devolución</label>
                    <Calendar id="date" value={devolutionDate} onChange={(e:any) => setDevolutionDate(e.value)} showIcon />
                </div>
            </Dialog>
        </div>
    );
};

export default Deliver;
