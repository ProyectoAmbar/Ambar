'use client';
import React, { useEffect, useState } from 'react';
import { Table, Modal, Form, Input, Select, Space } from 'antd';
import Swal from 'sweetalert2';
import withReactContent from 'sweetalert2-react-content';
import { BreadCrumb } from 'primereact/breadcrumb';
import { MenuItem } from 'primereact/menuitem';
import { getAllEmployees, createEmployee, updateEmployee, getEmployeeDataById, deleteEmployeeById } from '../../../api/taskService';
import { Button } from 'primereact/button';
import './taskview.scss';

const MySwal = withReactContent(Swal);

// export const config = { runtime: 'client' };

interface TaskType {
    key: number;
    id: string;
    name: string;
    description: string;
}

const UsersViewer = () => {
    const [tasks, setTasks] = useState<TaskType[]>([]);
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [currentUser, setCurrentUser] = useState(null);
    const [form] = Form.useForm();

    const home: MenuItem = { icon: 'pi pi-home', url: '/' };
    const breadcrumbItems: MenuItem[] = [{ label: 'Formularios' }, { label: 'Ver y Crear Tareas' }];

    useEffect(() => {
        fetchTasks();
    }, []);

    const fetchTasks = async () => {
        try {
            const data = await getAllEmployees();
            const formattedTasks = data.map((item: any, index: number) => ({
                key: index,
                id: item.id,
                name: item.usuario.nombreApellido,
                rol: item.usuario.rol.nombre
            }));
            setTasks(formattedTasks);
        } catch (error) {
            console.error('Error al cargar las tareas:', error);
        }
    };

    const showModal = async (user = null) => {
        setCurrentUser(user);
        if (user) {
            const userData = await getEmployeeDataById(user.id);
            console.log(userData);

            form.setFieldsValue({
                identificacion: userData.identificacion,
                sede: userData.sede,
                nombreApellido: userData.usuario.nombreApellido,
                correo: userData.usuario.correo,
                numeroCelular: userData.usuario.numeroCelular
            });
        } else {
            form.resetFields();
        }
        setIsModalVisible(true);
    };

    const rolId = {
        modista: '64a780574f5c1f4272d8e66c',
        lavanderia: '64c99d28bf3ae63b80f936e3',
        maquilladora: '653ea80670556042587486bd',
        admin: '648f6d5104e7df55bd457ccd',
        asesor: '64a8d3ef0c4dc9615b782391'
    };

    const handleOk = async () => {
        try {
            let values = await form.validateFields();
            if (currentUser) {
                await updateEmployee(currentUser.id, values);
            } else {
                const rolIdSeleccionado = values.rol;
                delete values.rol;
                console.log(values);
                await createEmployee(values, rolIdSeleccionado);
                MySwal.fire({
                    title: 'Usuario Creado',
                    text: 'El usuario ha sido creado exitosamente.',
                    icon: 'success'
                });
            }
            fetchTasks();
            setIsModalVisible(false);
        } catch (error) {
            console.error('Error al procesar el formulario:', error);
        }
    };

    const handleCancel = () => {
        setIsModalVisible(false);
    };

    const handleDelete = async (userId) => {
        MySwal.fire({
            title: '¿Estás seguro?',
            text: '¡No podrás revertir esta acción!',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Sí, bórralo!'
        }).then(async (result) => {
            if (result.isConfirmed) {
                await deleteEmployeeById(userId);
                fetchTasks();
                Swal.fire('¡Eliminado!', 'El usuario ha sido eliminado.', 'success');
            }
        });
    };

    const columns = [
        {
            title: 'ID',
            dataIndex: 'id',
            key: 'id'
        },
        {
            title: 'Nombre Trabajador',
            dataIndex: 'name',
            key: 'name'
        },
        {
            title: 'Rol',
            dataIndex: 'rol',
            key: 'rol'
        },
        {
            title: 'Acciones',
            key: 'actions',
            render: (_, record: any) => (
                <Space>
                    <Button onClick={() => showModal(record)}>Editar</Button>
                    <Button severity="danger" onClick={() => handleDelete(record.id)}>
                        Eliminar
                    </Button>
                </Space>
            )
        }
    ];

    return (
        <div className="containerFormTask">
            <div className="col-12 ">
                <div className="card">
                    <h5>Ver y Gestionar Usuarios</h5>
                    <BreadCrumb home={home} model={breadcrumbItems} />
                </div>
            </div>
            <div className="col-12 ">
                <div className="card">
                    <div className="buttonContainer">
                        <h5>Lista de Usuarios</h5>
                        <Button className="mb-2" onClick={() => showModal()} label="Crear Nuevo Usuario" severity="success" />{' '}
                    </div>
                    <Modal title={currentUser ? 'Editar Usuario' : 'Crear Usuario'} visible={isModalVisible} onOk={handleOk} onCancel={handleCancel}>
                        <Form form={form} layout="vertical">
                            <Form.Item name="identificacion" label="Identificación" rules={[{ required: false }]}>
                                <Input />
                            </Form.Item>
                            <Form.Item name="sede" label="Sede" rules={[{ required: false }]}>
                                <Input />
                            </Form.Item>
                            <Form.Item name="nombreApellido" label="Nombre y Apellido" rules={[{ required: false }]}>
                                <Input />
                            </Form.Item>
                            <Form.Item name="correo" label="Correo Electrónico" rules={[{ required: false }]}>
                                <Input type="email" />
                            </Form.Item>
                            <Form.Item name="numeroCelular" label="Número de Celular" rules={[{ required: false }]}>
                                <Input />
                            </Form.Item>
                            <Form.Item name="password" label="Contraseña" rules={[{ required: false }]}>
                                <Input.Password />
                            </Form.Item>
                            {!currentUser && (
                                <Form.Item name="rol" label="Rol" rules={[{ required: true }]}>
                                    <Select>
                                        {Object.entries(rolId).map(([key, value]) => (
                                            <Select.Option key={value} value={value}>
                                                {key}
                                            </Select.Option>
                                        ))}
                                    </Select>
                                </Form.Item>
                            )}
                        </Form>
                    </Modal>

                    <div className="table-responsive-container">
                        <Table columns={columns} dataSource={tasks} scroll={{ x: 1300 }} />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default UsersViewer;
