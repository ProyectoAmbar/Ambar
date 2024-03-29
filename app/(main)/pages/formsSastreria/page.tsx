'use client';
import React, { useCallback, useEffect, useRef, useState, useMemo } from 'react';
import { BreadCrumb } from 'primereact/breadcrumb';
import { MenuItem } from 'primereact/menuitem';
import { InputText } from 'primereact/inputtext';
import { TabView, TabPanel } from 'primereact/tabview';
import { Dropdown } from 'primereact/dropdown';
import { Button } from 'primereact/button';
import { getInfoArregloModista, getModistaArreglos, fetchModistaName, getProductobyCita } from '../../../api/taskService';
import Swal from 'sweetalert2';
import { enviarPrecios,responderTareaModistaComplete } from '../../../api/formServices';

interface CampoArreglo {
    arreglo: string;
    centimetros: string;
    precio: string;
}

interface DropdownItem {
    respuesta: string;
}

const FormSastreria = () => {
    const home: MenuItem = { icon: 'pi pi-home', url: '/' };
    const breadcrumbItems: MenuItem[] = [{ label: 'Formularios' }, { label: 'Sastreria' }];
    const [dropdownItem, setDropdownItem] = useState<DropdownItem | null>(null);
    const [dataArreglo, setDataArreglo] = useState(null);
    const [formMedidas, setFormMedidas] = useState(null);
    const [dataAsesorr, setDataAsesor] = useState(null);
    const [ProductoData, setProductoData] = useState(null);
    const [preciosVisuales, setPreciosVisuales] = useState({});

    const dropdownItems: DropdownItem[] = useMemo(() => [{ respuesta: 'Si' }, { respuesta: 'No' }], []);

    useEffect(() => {
        setDropdownItem(dropdownItems[0]);
    }, [dropdownItems]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await getInfoArregloModista();
                setDataArreglo(data);
            } catch (error) {
                console.error('Error al obtener datos: ', error);
            }
        };

        fetchData();
    }, []);

    useEffect(() => {
        const fetchFormMedidas = async () => {
            try {
                const formMedidas = await getModistaArreglos(dataArreglo.formMedidas);
                setFormMedidas(formMedidas);
                const dataAsesor = await fetchModistaName(formMedidas.asesor);
                setDataAsesor(dataAsesor);
                const producto = await getProductobyCita(dataArreglo && dataArreglo.producto);
                setProductoData(producto);
            } catch (error) {
                console.error('Error al obtener formMedidas: ', error);
            }
        };

        if (dataArreglo) {
            fetchFormMedidas();
        }
    }, [dataArreglo]);

    const handlePrecioChange = (index, nuevoPrecioVisual) => {
        const nuevosPreciosVisuales = { ...preciosVisuales, [index]: nuevoPrecioVisual };
        setPreciosVisuales(nuevosPreciosVisuales);

        const nuevoValorNumerico = parseFloat(nuevoPrecioVisual.replace(/\D/g, '')) || 0;
        const nuevasFormMedidas = { ...formMedidas };
        nuevasFormMedidas.arreglos[index].precio = nuevoValorNumerico;
        setFormMedidas(nuevasFormMedidas);
    };

    const formatearComoCOP = (valor) => {
        if (!valor) return '';
        const numero = parseFloat(valor);
        return new Intl.NumberFormat('es-CO', {
            style: 'currency',
            currency: 'COP',
            minimumFractionDigits: 0
        }).format(numero);
    };

    useEffect(() => {
        if (formMedidas && formMedidas.arreglos) {
            const preciosIniciales = formMedidas.arreglos.reduce((acc, arreglo, index) => {
                acc[index] = formatearComoCOP(arreglo.precio);
                return acc;
            }, {});
            setPreciosVisuales(preciosIniciales);
        }
    }, [formMedidas]);

    const enviarDatos = async () => {
        const datosParaEnviar = {
            arreglos: formMedidas && formMedidas.arreglos.map((arreglo) => ({ precio: arreglo.precio }))
        };
    
        try {
            const resultado = await enviarPrecios(datosParaEnviar, dataArreglo.formMedidas);
            console.log('Datos enviados con éxito', resultado);
    
            const completarTarea = async () => {
                try {
                    await responderTareaModistaComplete({ completado: true });
                    console.log("Tarea completada con éxito");
                } catch (error) {
                    console.error("Error al completar la tarea: ", error);
                    throw error; 
                }
            };
    
            Swal.fire({
                title: '¡Éxito!',
                text: 'Producto arreglado con precios enviados',
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
    

    return (
        <div>
            <div className="col-12">
                <div className="card">
                    <h5>Formulario Sastreria</h5>
                    <BreadCrumb home={home} model={breadcrumbItems} />
                </div>
            </div>

            <div className="col-12">
                <TabView>
                    <TabPanel header="Formulario Medidas">
                        <div className="p-fluid formgrid grid formmedidas">
                            <div className="field col-12 md:col-6">
                                <label htmlFor="fechaentre">Fecha entrega</label>
                                <InputText id="fechaentre" type="text" readOnly value={dataArreglo && dataArreglo.fecha} />
                            </div>

                            <div className="field col-12 md:col-6">
                                <label htmlFor="producto">Producto</label>
                                <InputText id="producto" type="text" value={ProductoData && ProductoData.nombre} readOnly />
                            </div>
                            <div className="field col-12 md:col-6">
                                <label htmlFor="Asesorid">Asesora</label>
                                <InputText id="Asesorid" type="text" value={dataAsesorr && dataAsesorr.usuario.nombreApellido} readOnly />
                            </div>
                            <div className="field col-12 md:col-6">
                                <label htmlFor="arreglosNeed">Necesita Arreglos</label>
                                <InputText id="arreglosNeed" type="text" value={formMedidas && formMedidas.arreglos && formMedidas.arreglos.length > 0 ? 'Si' : 'No'} readOnly />
                            </div>
                            {formMedidas &&
                                formMedidas.arreglos.map((arreglo: any, index: any) => (
                                    <React.Fragment key={index}>
                                        <div className="field col-12 md:col-6">
                                            <label htmlFor={`arreglo-${index}`}>Arreglo</label>
                                            <InputText id={`arreglo-${index}`} type="text" value={arreglo.mensaje} readOnly />
                                        </div>
                                        <div className="field col-12 md:col-3">
                                            <label htmlFor={`cm-${index}`}>Centímetros</label>
                                            <InputText id={`cm-${index}`} type="text" value={arreglo.cm} readOnly />
                                        </div>
                                        <div className="field col-12 md:col-3">
                                            <label htmlFor={`precio-${index}`}>Precio</label>
                                            <InputText id={`precio-${index}`} type="text" value={preciosVisuales[index] || ''} onChange={(e) => handlePrecioChange(index, e.target.value)} />
                                        </div>
                                    </React.Fragment>
                                ))}
                            <div className="field col-12 md:col-4">
                                <div className="field col-12 md:col-4 buttonform">
                                    <Button label="producto Arreglado" severity="success" onClick={enviarDatos} />
                                </div>
                            </div>
                        </div>
                    </TabPanel>
                    <TabPanel header="Datos Alquiler">
                        <div className="p-fluid formgrid grid">
                            <div className="field col-12 md:col-6">
                                <label htmlFor="Asesorid">Nombre </label>
                                <InputText id="Asesorid" type="text" />
                            </div>
                            <div className="field col-12 md:col-6">
                                <label htmlFor="Asesorid">Apellido </label>
                                <InputText id="Asesorid" type="text" />
                            </div>
                            <div className="field col-12 md:col-6">
                                <label htmlFor="email">Correo Electronico</label>
                                <InputText id="email" type="text" />
                            </div>
                            <div className="field col-12 md:col-3">
                                <label htmlFor="identificacion">Identificacion</label>
                                <InputText id="identificacion" type="text" />
                            </div>
                            <div className="field col-12 md:col-3">
                                <label htmlFor="phone">Celular</label>
                                <InputText id="phone" type="text" />
                            </div>
                            <div className="field col-12 md:col-6">
                                <label htmlFor="Direccion">Direccion</label>
                                <InputText id="Direccion" type="text" />
                            </div>
                            <div className="field col-12 md:col-3">
                                <label htmlFor="textcd">Numero Factura</label>
                                <InputText id="text" type="text" />
                            </div>
                            <div className="field col-12 md:col-3">
                                <label htmlFor="textcd">Fecha Factura</label>
                                <InputText id="text" type="text" />
                            </div>
                            <div className="field col-12 md:col-6">
                                <label htmlFor="textcd">Fecha Cita Medida</label>
                                <InputText id="text" type="text" />
                            </div>
                            <div className="field col-12 md:col-6">
                                <label htmlFor="textcd">Fecha Entrega</label>
                                <InputText id="text" type="text" />
                            </div>
                            <div className="field col-12 md:col-3">
                                <label htmlFor="idVesti">Referencia Vestido o Traje</label>
                                <InputText id="text" type="text" />
                            </div>
                            <div className="field col-12 md:col-3">
                                <label htmlFor="idVesti">Categoria</label>
                                <InputText id="text" type="text" />
                            </div>
                            <div className="field col-12 md:col-6">
                                <label htmlFor="idVesti">Color</label>
                                <InputText id="text" type="text" />
                            </div>
                            <div className="field col-12 md:col-6">
                                <label htmlFor="idVesti">Accesorio</label>
                                <InputText id="text" type="text" />
                            </div>
                            <div className="field col-12 md:col-3">
                                <label htmlFor="idVesti">Acompañante</label>
                                <InputText id="text" type="text" />
                            </div>
                            <div className="field col-12 md:col-3">
                                <label htmlFor="idVesti">2do Acompañante</label>
                                <InputText id="text" type="text" />
                            </div>
                            <div className="field col-12 md:col-3">
                                <label htmlFor="idVesti">Metodo Pago</label>
                                <InputText id="text" type="text" />
                            </div>
                            <div className="field col-12 md:col-3">
                                <label htmlFor="idVesti">Total Alquiler</label>
                                <InputText id="text" type="text" />
                            </div>
                            <div className="field col-12 md:col-6">
                                <label htmlFor="idVesti">Abono</label>
                                <InputText id="text" type="text" />
                            </div>
                            <div className="field col-12 md:col-3">
                                <label htmlFor="idVesti">Saldo Restante</label>
                                <InputText id="text" type="text" />
                            </div>
                            <div className="field col-12 md:col-3">
                                <label htmlFor="idVesti">Deposito</label>
                                <InputText id="text" type="text" />
                            </div>
                            <div className="field col-12 md:col-3">
                                <label htmlFor="idVesti">Id Asesora Comercial</label>
                                <InputText id="text" type="text" />
                            </div>
                            <div className="field col-12 md:col-3">
                                <label htmlFor="idVesti">Nombre</label>
                                <InputText id="text" type="text" />
                            </div>
                        </div>
                    </TabPanel>
                </TabView>
            </div>
        </div>
    );
};

export default FormSastreria;
