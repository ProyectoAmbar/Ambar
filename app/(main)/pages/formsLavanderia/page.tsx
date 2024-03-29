'use client';
import React, { useCallback, useEffect, useRef, useState, useMemo } from 'react';
import { BreadCrumb } from 'primereact/breadcrumb';
import { MenuItem } from 'primereact/menuitem';
import { InputText } from 'primereact/inputtext';
import { TabView, TabPanel } from 'primereact/tabview';
import { Dropdown } from 'primereact/dropdown';
import { Button } from 'primereact/button';
import { Calendar } from 'primereact/calendar';
import { GetTareaLavanderia, getformAlquiler, fetchProductoName } from '../../../api/taskService';

import {responderTareaLavanderiaComplete} from '../../../api/formServices';
import Swal from 'sweetalert2';

interface CampoArreglo {
    arreglo: string;
    centimetros: string;
    precio: string;
}

interface DropdownItem {
    respuesta: string;
}

const Formlavanderia = () => {
    const home: MenuItem = { icon: 'pi pi-home', url: '/' };
    const breadcrumbItems: MenuItem[] = [{ label: 'Formularios' }, { label: 'Lavanderia' }];
    const [arreglos, setArreglos] = useState<Array<{ arreglo: string; centimetros: string; precio: string }>>([]);
    const [dropdownItem, setDropdownItem] = useState<DropdownItem | null>(null);
    const [calendarValue1, setCalendarValue1] = useState<string | Date | Date[] | null>(null);
    const [formAlquilerData, setformAlquilerData] = useState(null);
    const [producto, setProducto] = useState(null);
    const [TareaLavanderiaS, setTareaLavanderia] = useState(null);

    const handleArregloChange = (index: number, field: keyof CampoArreglo, value: string) => {
        const newArr = [...arreglos];
        newArr[index][field] = value;
        setArreglos(newArr);
    };

    const addArregloField = () => {
        setArreglos([...arreglos, { arreglo: '', centimetros: '', precio: '' }]);
    };
    const deleteLastArregloField = () => {
        const newArr = [...arreglos];
        newArr.pop();
        setArreglos(newArr);
    };

    const dropdownItems: DropdownItem[] = useMemo(() => [{ respuesta: 'Si' }, { respuesta: 'No' }], []);

    const fetchData = async () => {
        try {
            const TareaLavanderia = await GetTareaLavanderia();
            setTareaLavanderia(TareaLavanderia);
            const formAlquiler = await getformAlquiler(TareaLavanderia.formulario);
            setformAlquilerData(formAlquiler);

            const Producto = await fetchProductoName(TareaLavanderia.producto);
            setProducto(Producto);
        } catch (error) {
            console.error('Error al obtener los datos: ', error);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    const completarTarea = async () => {
        try {
            await responderTareaLavanderiaComplete({ completado: true });

            console.log('Tarea completada con éxito');
            Swal.fire({
                title: '¡Éxito!',
                text: 'Producto Lavado ',
                icon: 'success',
                confirmButtonText: 'Ok'
            }).then(() => {
                completarTarea().then(() => {
                    window.location.href = '/';
                });
            });
        } catch (error) {
            console.error('Error al enviar datos: ', error);
            Swal.fire({
                title: 'Error',
                text: 'No se pudo enviar la información',
                icon: 'error',
                confirmButtonText: 'Ok'
            });
        }
    };

    // En tu componente JSX (parte del renderizado)
    <Button onClick={completarTarea}>Completar Tarea</Button>;

    useEffect(() => {
        setDropdownItem(dropdownItems[0]);
    }, [dropdownItems]);

    return (
        <div>
            <div className="col-12">
                <div className="card">
                    <h5>Formulario Lavanderia</h5>
                    <BreadCrumb home={home} model={breadcrumbItems} />
                </div>
            </div>

            <div className="col-12">
                <TabView>
                    <TabPanel header="Formulario Sastreria">
                        <div className="p-fluid formgrid grid formmedidas">
                            <div className="field col-12 md:col-6">
                                <label htmlFor="factur">Factura</label>
                                <InputText id="factur" type="text" value={formAlquilerData && formAlquilerData.numeroFactura} readOnly />
                            </div>
                            <div className="field col-12 md:col-6">
                                <label htmlFor="referenciaproduc">Referencia</label>
                                <InputText id="referenciaproduc" type="text" value={producto && producto.referencia} readOnly />
                            </div>
                            <div className="field col-12 md:col-6">
                                <label htmlFor="colorproduc">Color</label>
                                <InputText id="colorproduc" type="text" value={producto && producto.color} readOnly />
                            </div>

                            <div className="field col-12 md:col-6">
                                <label htmlFor="fechalimit">Fecha Entrega Limite </label>
                                <InputText id="fechalimit" type="text" readOnly value={TareaLavanderiaS && TareaLavanderiaS.fecha} />
                            </div>
                            <div className="field col-12 md:col-6">
                                <h5>Fecha Entrega</h5>
                                <Calendar showIcon showButtonBar value={calendarValue1} onChange={(e) => setCalendarValue1(e.value ?? null)} />
                            </div>
                            <div className="field col-12 md:col-4">
                                <div className="field col-12 md:col-4 buttonform">
                                    <Button label="Producto Listo" severity="success" onClick={completarTarea} />
                                </div>
                            </div>
                        </div>
                    </TabPanel>
                </TabView>
            </div>
        </div>
    );
};

export default Formlavanderia;
