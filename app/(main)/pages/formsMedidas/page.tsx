'use client';
import React, { useCallback, useEffect, useRef, useState, useMemo } from 'react';
import { BreadCrumb } from 'primereact/breadcrumb';
import { MenuItem } from 'primereact/menuitem';
import { InputText } from 'primereact/inputtext';
import { TabView, TabPanel } from 'primereact/tabview';
import { Dropdown } from 'primereact/dropdown';
import { Button } from 'primereact/button';
import { Calendar } from 'primereact/calendar';
import { getTareaCitaMedidasById, getFormByCitaMedidas, getAsesorByCita, getProductobyCita } from '../../../api/taskService';
import './styles.scss';
import Swal from 'sweetalert2';
import { postCitaMedidas } from '../../../api/formServices';
interface CampoArreglo {
    arreglo: string;
    centimetros: string;
    precio: string;
}

interface DropdownItem {
    respuesta: string;
}

const FormMedida = () => {
    const home: MenuItem = { icon: 'pi pi-home', url: '/' };
    const breadcrumbItems: MenuItem[] = [{ label: 'Formularios' }, { label: 'Toma de medidas y Arreglos' }];
    const [arreglos, setArreglos] = useState<Array<{ arreglo: string; centimetros: string; precio: string }>>([]);
    const [dropdownItem, setDropdownItem] = useState<DropdownItem | null>(null);

    //Info A mostrar y enviar
    const [nombre, setNombre] = useState('');
    const [apellido, setApellido] = useState('');
    const [identificacion, setIdentificacion] = useState('');
    const [celular, setCelular] = useState('');
    const [NumFactu, setNumFactu] = useState('');
    const [FechaFactu, setFechaFactu] = useState('');
    const [FechaEntrega, setFechaEntrega] = useState('');
    const [email, setEmail] = useState('');
    const [direccion, setDireccion] = useState('');
    const [FechaCita, setFechaCita] = useState('');
    const [accesorio, setAccesorio] = useState('');
    const [PrimererAcompa, setPrimererAcompa] = useState('');
    const [SegunAcompa, setSegunAcompa] = useState('');
    const [metodoPago, setmetodoPago] = useState('');
    const [TotalAlquiler, setTotalAlquiler] = useState('');
    const [abono, setAbono] = useState('');
    const [SaldoRestante, setSaldoRestante] = useState('');
    const [deposito, setDeposito] = useState('');
    const [asesor, setAsesor] = useState('');
    const [asesorid, setAsesorId] = useState('');
    const [nomProduc, setnomProduc] = useState('');
    const [colorProduc, setColorProduct] = useState('');
    const [referenciaProduct, setReferenciaProduct] = useState('');
    const [necesitaNuevaCita, setNecesitaNuevaCita] = useState(null);
    const [fechaCitaNueva, setFechaCitaNueva] = useState<string | Date | Date[] | null>(null);

    const handleArregloChange = (index: number, field: keyof CampoArreglo, value: string) => {
        const newArr = [...arreglos];
        newArr[index][field] = value;
        setArreglos(newArr);
    };

    const opcionesNuevaCita = [
        { label: 'Sí', value: 'Si' },
        { label: 'No', value: 'No' }
    ];
    const addArregloField = () => {
        setArreglos([...arreglos, { arreglo: '', centimetros: '', precio: '' }]);
    };
    const deleteLastArregloField = () => {
        const newArr = [...arreglos];
        newArr.pop();
        setArreglos(newArr);
    };

    const dropdownItems: DropdownItem[] = useMemo(() => [{ respuesta: 'Si' }, { respuesta: 'No' }], []);

    useEffect(() => {
        setDropdownItem(dropdownItems[0]);
    }, [dropdownItems]);

    useEffect(() => {
        const TraerFormAlquiler = async () => {
            try {
                const getTareaCitaMedidas = await getTareaCitaMedidasById();
                console.log(getTareaCitaMedidas);
                const formData = await getFormByCitaMedidas(getTareaCitaMedidas.formulario);
                console.log(formData);
                setNombre(formData.nombre);
                setApellido(formData.apellido);
                setIdentificacion(formData.identificacion);
                setCelular(formData.celular);
                setNumFactu(formData.numeroFactura);
                setFechaFactu(formData.fechaDeFactura);
                setFechaEntrega(formData.fechaDeEntrega);
                setEmail(formData.correo);
                setDireccion(formData.direccion);
                setFechaCita(formData.FechaCitaDeMedidas);
                setAccesorio(formData.accesorio);
                setPrimererAcompa(formData.aro);
                setSegunAcompa(formData.velo);
                setmetodoPago(formData.metodoDePago);
                setTotalAlquiler(formData.total);
                setAbono(formData.abono);
                setSaldoRestante(formData.saldo);
                setDeposito(formData.deposito);

                const asesor = await getAsesorByCita(formData.asesor);
                const producto = await getProductobyCita(formData.Producto);

                setAsesor(asesor.usuario.nombreApellido);
                setAsesorId(asesor.id);
                setnomProduc(producto.nombre);
                setColorProduct(producto.color);
                setReferenciaProduct(producto.referencia);
            } catch (error) {
                console.error('Error al cargar las tareas:', error);
            }
        };

        TraerFormAlquiler();
    }, []);

    const formatearComoCOP = (valor: any) => {
        return new Intl.NumberFormat('es-CO', {
            style: 'currency',
            currency: 'COP',
            minimumFractionDigits: 0
        }).format(valor);
    };

    const handleSubmit = async () => {
        const formatDateComponents = (date: any) => {
            if (!date) return { year: null, month: null, day: null };

            const d = new Date(date);
            return {
                year: d.getFullYear(),
                month: `0${d.getMonth() + 1}`.slice(-2),
                day: `0${d.getDate()}`.slice(-2)
            };
        };

        const { year: añoCitaMedidas, month: mesCitaMedidas, day: diaCitaMedidas } = necesitaNuevaCita === 'Si' ? formatDateComponents(fechaCitaNueva) : { year: null, month: null, day: null };

        const arreglosData =
            dropdownItem?.respuesta === 'Si'
                ? arreglos.map((arreglo) => ({
                      mensaje: arreglo.arreglo,
                      cm: parseInt(arreglo.centimetros),
                      precio: null
                  }))
                : [];

        const dataToSend = {
            estado: true,
            necesitaModista: dropdownItem?.respuesta === 'Si',
            nuevaCita: necesitaNuevaCita === 'Si',
            arreglos: arreglosData,
            añoCitaMedidas,
            mesCitaMedidas: mesCitaMedidas ? parseInt(mesCitaMedidas, 10) : null,
            diaCitaMedidas: diaCitaMedidas ? parseInt(diaCitaMedidas, 10) : null
        };

        console.log('Datos a enviar:', dataToSend);

        try {
            const response = await postCitaMedidas(dataToSend);
            console.log(response, 'holaa');
            Swal.fire({
                title: 'Éxito',
                text: 'Formulario enviado correctamente',
                icon: 'success',
                confirmButtonText: 'OK'
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = '/';
                }
            });
        } catch (error) {
            console.error('Error al enviar el formulario:', error);
        }
    };

    return (
        <div>
            <div className="col-12">
                <div className="card">
                    <h5>Formulario Toma Medidas</h5>
                    <BreadCrumb home={home} model={breadcrumbItems} />
                </div>
            </div>

            <div className="col-12">
                <TabView>
                    <TabPanel header="Formulario Medidas">
                        <div className="p-fluid formgrid grid formmedidas">
                            <div className="field col-12 md:col-6">
                                <label htmlFor="fechaEntrega">Fecha Entrega</label>
                                <InputText id="fechaEntrega" type="text" value={FechaEntrega} onChange={(e) => setFechaEntrega(e.target.value)} readOnly />
                            </div>
                            <div className="field col-12 md:col-6">
                                <label htmlFor="catego">Categoria</label>
                                <InputText id="catego" type="text" value={nomProduc} onChange={(e) => setnomProduc(e.target.value)} readOnly />
                            </div>
                            <div className="field col-12 md:col-6">
                                <label htmlFor="Asesorid">Asesora</label>
                                <InputText id="Asesorid" type="text" value={asesor} onChange={(e) => setAsesor(e.target.value)} readOnly />
                            </div>
                            <div className="field col-12 md:col-6">
                                <label htmlFor="nuevaCita">Requiere Nueva Cita de Medidas</label>
                                <Dropdown id="nuevaCita" value={necesitaNuevaCita} options={opcionesNuevaCita} onChange={(e) => setNecesitaNuevaCita(e.value)} optionLabel="label" placeholder="Selecciona una opción" />
                            </div>
                            {necesitaNuevaCita === 'Si' && (
                                <div className="field col-12 md:col-6">
                                    <h5>Fecha Cita Medidas</h5>
                                    <Calendar showIcon showButtonBar value={fechaCitaNueva} onChange={(e) => setFechaCitaNueva(e.value ?? null)} />
                                </div>
                            )}

                            <div className="field col-12 md:col-6">
                                <label htmlFor="arreglosneed">Necesita Arreglos?</label>
                                <Dropdown id="arreglosneed" value={dropdownItem} onChange={(e) => setDropdownItem(e.value)} options={dropdownItems} optionLabel="respuesta" placeholder="Selecciona uno"></Dropdown>
                            </div>

                            {dropdownItem?.respuesta === 'Si' && (
                                <>
                                    {arreglos.map((arreglo, index) => (
                                        <React.Fragment key={index}>
                                            <div className="field col-12 md:col-6">
                                                <label htmlFor={`arreglo${index}`}>Arreglo</label>
                                                <InputText id={`arreglo${index}`} type="text" value={arreglo.arreglo} onChange={(e) => handleArregloChange(index, 'arreglo', e.target.value)} />
                                            </div>
                                            <div className="field col-12 md:col-3">
                                                <label htmlFor={`centimetros${index}`}>Centímetros</label>
                                                <InputText id={`centimetros${index}`} type="text" value={arreglo.centimetros} onChange={(e) => handleArregloChange(index, 'centimetros', e.target.value)} />
                                            </div>
                                            <div className="field col-12 md:col-3">
                                                <label htmlFor={`precio${index}`}>Precio</label>
                                                <InputText id={`precio${index}`} type="text" value={arreglo.precio} onChange={(e) => handleArregloChange(index, 'precio', e.target.value)} readOnly />
                                            </div>
                                        </React.Fragment>
                                    ))}
                                    <div className="field col-12 md:col-3 centrado ">
                                        <div className="field col-12 md:col-12 buttonform centrado ">
                                            <Button label="Agregar Arreglo" onClick={addArregloField} />
                                        </div>
                                    </div>
                                    <div className="field col-12 md:col-3 centrado ">
                                        <div className="field col-12 md:col-12 buttonform centrado">
                                            <Button label="Eliminar Arreglo" severity="danger" onClick={deleteLastArregloField} />
                                        </div>
                                    </div>
                                </>
                            )}

                            <div className="field col-12 md:col-4 flex items-center pb-0 mb-0">
                                <div className="field col-12 md:col-4 buttonform flex items-center pb-0 mb-0">
                                    <Button label="Guardar" severity="success" onClick={handleSubmit} />
                                </div>
                            </div>
                        </div>
                    </TabPanel>
                    <TabPanel header="Datos Alquiler">
                        <div className="p-fluid formgrid grid">
                            <div className="field col-12 md:col-6">
                                <label htmlFor="nombre">Nombre</label>
                                <InputText id="nombre" type="text" value={nombre} onChange={(e) => setNombre(e.target.value)} readOnly />
                            </div>
                            <div className="field col-12 md:col-6">
                                <label htmlFor="apellido">Apellido</label>
                                <InputText id="apellido" type="text" value={apellido} onChange={(e) => setApellido(e.target.value)} readOnly />
                            </div>
                            <div className="field col-12 md:col-6">
                                <label htmlFor="email">Correo Electrónico</label>
                                <InputText id="email" type="text" value={email} onChange={(e) => setEmail(e.target.value)} readOnly />
                            </div>
                            <div className="field col-12 md:col-3">
                                <label htmlFor="identificacion">Identificación</label>
                                <InputText id="identificacion" type="text" value={identificacion} onChange={(e) => setIdentificacion(e.target.value)} readOnly />
                            </div>
                            <div className="field col-12 md:col-3">
                                <label htmlFor="phone">Celular</label>
                                <InputText id="phone" type="text" value={celular} onChange={(e) => setCelular(e.target.value)} readOnly />
                            </div>
                            <div className="field col-12 md:col-6">
                                <label htmlFor="Direccion">Direccion</label>
                                <InputText id="Direccion" type="text" value={direccion} onChange={(e) => setDireccion(e.target.value)} readOnly />
                            </div>
                            <div className="field col-12 md:col-3">
                                <label htmlFor="numfact">Numero Factura</label>
                                <InputText id="numfact" type="text" value={NumFactu} onChange={(e) => setNumFactu(e.target.value)} readOnly />
                            </div>
                            <div className="field col-12 md:col-3">
                                <label htmlFor="fechafact">Fecha Factura</label>
                                <InputText id="fechafact" type="text" value={FechaFactu} onChange={(e) => setFechaFactu(e.target.value)} readOnly />
                            </div>
                            <div className="field col-12 md:col-6">
                                <label htmlFor="fechaCita">Fecha Cita Medida</label>
                                <InputText id="fechaCita" type="text" value={FechaCita} onChange={(e) => setFechaCita(e.target.value)} readOnly />
                            </div>
                            <div className="field col-12 md:col-6">
                                <label htmlFor="fechaEntrega">Fecha Entrega</label>
                                <InputText id="fechaEntrega" type="text" value={FechaEntrega} onChange={(e) => setFechaEntrega(e.target.value)} readOnly />
                            </div>
                            <div className="field col-12 md:col-3">
                                <label htmlFor="referenciaProduc">Referencia Vestido o Traje</label>
                                <InputText id="referenciaProduc" type="text" value={referenciaProduct} onChange={(e) => setReferenciaProduct(e.target.value)} readOnly />
                            </div>
                            <div className="field col-12 md:col-3">
                                <label htmlFor="cate">Categoria</label>
                                <InputText id="cate" type="text" value={nomProduc} onChange={(e) => setnomProduc(e.target.value)} readOnly />
                            </div>
                            <div className="field col-12 md:col-6">
                                <label htmlFor="colorProduc">Color</label>
                                <InputText id="colorProduc" type="text" value={colorProduc} onChange={(e) => setColorProduct(e.target.value)} readOnly />
                            </div>
                            <div className="field col-12 md:col-6">
                                <label htmlFor="accesori">Accesorio</label>
                                <InputText id="accesori" type="text" value={accesorio} onChange={(e) => setAccesorio(e.target.value)} readOnly />
                            </div>
                            <div className="field col-12 md:col-3">
                                <label htmlFor="acompa">Acompañante</label>
                                <InputText id="acompa" type="text" value={PrimererAcompa} onChange={(e) => setPrimererAcompa(e.target.value)} readOnly />
                            </div>
                            <div className="field col-12 md:col-3">
                                <label htmlFor="acompa2">2do Acompañante</label>
                                <InputText id="acompa2" type="text" value={SegunAcompa} onChange={(e) => setSegunAcompa(e.target.value)} readOnly />
                            </div>
                            <div className="field col-12 md:col-3">
                                <label htmlFor="metodo">Metodo Pago</label>
                                <InputText id="metodo" type="text" value={metodoPago} onChange={(e) => setmetodoPago(e.target.value)} readOnly />
                            </div>
                            <div className="field col-12 md:col-3">
                                <label htmlFor="total">Total Alquiler</label>
                                <InputText id="total" type="text" value={formatearComoCOP(TotalAlquiler)} onChange={(e) => setTotalAlquiler(e.target.value)} readOnly />
                            </div>
                            <div className="field col-12 md:col-6">
                                <label htmlFor="abono">Abono</label>
                                <InputText id="abono" type="text" value={formatearComoCOP(abono)} onChange={(e) => setAbono(e.target.value)} readOnly />
                            </div>
                            <div className="field col-12 md:col-3">
                                <label htmlFor="saldo">Saldo Restante</label>
                                <InputText id="saldo" type="text" value={formatearComoCOP(SaldoRestante)} onChange={(e) => setSaldoRestante(e.target.value)} readOnly />
                            </div>
                            <div className="field col-12 md:col-3">
                                <label htmlFor="deposi">Deposito</label>
                                <InputText id="deposi" type="text" value={formatearComoCOP(deposito)} onChange={(e) => setDeposito(e.target.value)} readOnly />
                            </div>
                            <div className="field col-12 md:col-3">
                                <label htmlFor="idVesti">Id Asesora Comercial</label>
                                <InputText id="text" type="text" value={asesorid} onChange={(e) => setAsesorId(e.target.value)} readOnly />
                            </div>
                            <div className="field col-12 md:col-3">
                                <label htmlFor="idVesti">Nombre</label>
                                <InputText id="text" type="text" value={asesor} onChange={(e) => setAsesor(e.target.value)} readOnly />
                            </div>
                        </div>
                    </TabPanel>
                </TabView>
            </div>
        </div>
    );
};

export default FormMedida;
