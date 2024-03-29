'use client';
import React, { useState, useEffect, useMemo } from 'react';
import { InputText } from 'primereact/inputtext';
import { Button } from 'primereact/button';
import { InputTextarea } from 'primereact/inputtextarea';
import { Dropdown } from 'primereact/dropdown';
import { BreadCrumb } from 'primereact/breadcrumb';
import { MenuItem } from 'primereact/menuitem';
import { useRouter } from 'next/router';
import { Calendar } from 'primereact/calendar';
import { RadioButton } from 'primereact/radiobutton';
import { Checkbox, CheckboxChangeEvent } from 'primereact/checkbox';
import { locale } from 'primereact/api';
import Cookies from 'js-cookie';
import { getProducts } from '../../../api/formServices';
import Swal from 'sweetalert2';
import { postFormulario } from '../../../api/formServices';
import { cookies } from 'next/dist/client/components/headers';

interface DropdownItem {
    name: string;
    code: string;
}

interface Producto {
    _id: string;
    nombre: string;
    referencia: string;
    color: string;
}

const Alquiler = () => {
    const home: MenuItem = { icon: 'pi pi-home', url: '/' };
    const breadcrumbItems: MenuItem[] = [{ label: 'Formularios' }, { label: 'Alquiler Trajes y Vestidos' }];
    const [calendarValue4, setCalendarValue4] = useState<string | Date | Date[] | null>(null);
    const [checkboxValue, setCheckboxValue] = useState<string[]>([]);
    const idrol = Cookies.get('idRol');
    // Estados para los productos a usar

    const [productos, setProductos] = useState<Producto[]>([]);
    const [productoFiltrado, setProductoFiltrado] = useState<Producto | null>(null);
    const [productoId, setProductoId] = useState<Producto | null>(null);
    const [debouncedRef, setDebouncedRef] = useState('');
    const [abonoRaw, setAbonoRaw] = useState(0);
    const [depositoRaw, setDepositoRaw] = useState(0);

    // Value to sent
    const [nombre, setNombre] = useState('');
    const [apellido, setApellido] = useState('');
    const [identificacion, setIdentificacion] = useState('');
    const [phone, setPhone] = useState('');
    const [direccion, setDireccion] = useState('');
    const [numFactur, setNumFactur] = useState('');
    const [email, setEmail] = useState('');
    const [referencia, setReferencia] = useState('');
    const sede: string = 'villavicencio';
    const [totalAlquiler, setTotalAlquiler] = useState('');
    const [abono, setAbono] = useState('');
    const [saldoRestante, setSaldoRestante] = useState('');
    const [totalAlquilerRaw, setTotalAlquilerRaw] = useState(0);
    const [radioValueAcompa, setRadioValueAcompa] = useState(null);
    const [radioValue2doAcompa, setRadioValue2doAcompa] = useState(null);
    const [deposito, setDeposito] = useState('');
    const [calendarValue1, setCalendarValue1] = useState<string | Date | Date[] | null>(null);
    const [calendarValue2, setCalendarValue2] = useState<string | Date | Date[] | null>(null);
    const [dropdownItem, setDropdownItem] = useState<DropdownItem | null>(null);
    const [dropdownItem2, setDropdownItem2] = useState<DropdownItem | null>(null);

    //Informacion Asesor
    const idAsesor = Cookies.get('userId');
    const nombreAsesor = Cookies.get('nombreApellido');
    const idEmpleado = Cookies.get('idEmpleado');
    const dropdownItems: DropdownItem[] = useMemo(
        () => [
            { name: 'Tiara', code: 'Tiara' },
            { name: 'Corbatin', code: 'Corbatin' },
            { name: 'Corbata', code: 'Corbata' },
            { name: 'Pañueñulo', code: 'Pañueñulo' },
            { name: 'No Acompañante', code: 'NoAcompañante' }
        ],
        []
    );

    useEffect(() => {
        setDropdownItem(dropdownItems[0]);
    }, [dropdownItems]);

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                const response = await getProducts();
                console.log('Productos recibidos:', response);
                setProductos(response);
            } catch (error) {
                console.error('Error al obtener productos:', error);
            }
        };

        fetchProducts();
    }, []);

    useEffect(() => {
        const timerId = setTimeout(() => {
            setDebouncedRef(referencia);
        }, 500); 
        return () => {
            clearTimeout(timerId);
        };
    }, [referencia]);

    useEffect(() => {
        if (debouncedRef !== '') {
            const filteredProduct:any = productos.find((producto) => producto.referencia == debouncedRef);
            if (filteredProduct) {
                setProductoFiltrado(filteredProduct);
                if (!filteredProduct.disponible) {
                    alert('No se puede alquilar el producto que no es disponible por el momento.');
                    setReferencia('');
                setDebouncedRef(''); 
                }
            } else {
                setProductoFiltrado(null);
            }
        } else {
            setProductoFiltrado(null);
        }
    }, [debouncedRef, productos]);

    const handleReferenciaChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setReferencia(e.target.value.trim());
    };

    const dropdownItems2: DropdownItem[] = useMemo(
        () => [
            { name: 'Efectivo', code: 'Efectivo' },
            { name: 'Tarjeta', code: 'Tarjeta' }
        ],
        []
    );

    useEffect(() => {
        setDropdownItem2(dropdownItems2[0]);
    }, [dropdownItems2]);

    {
        /*  const onCheckboxChange = (e: CheckboxChangeEvent) => {
        let selectedValue = [...checkboxValue];
        if (e.checked) selectedValue.push(e.value);
        else selectedValue.splice(selectedValue.indexOf(e.value), 1);

        setCheckboxValue(selectedValue);
    };*/
    }

    const onCheckboxChange = (e: any) => {
        const value = e.target.value;

        if (checkboxValue.includes(value)) {
            setCheckboxValue((prevValues) => prevValues.filter((item) => item !== value));
        } else {
            setCheckboxValue([value]);
        }
    };

    //Funcion para los abonos

    // Función para formatear el número como moneda para visualización.
    const formatCurrency = (value: number) => {
        return value.toLocaleString('es-CO', { style: 'currency', currency: 'COP', minimumFractionDigits: 0 });
    };

    // Manejadores para los eventos de cambio de los campos de texto. Estos manejan los valores sin formato.
    const handleTotalAlquilerChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const total = e.target.value.replace(/\D/g, '');
        setTotalAlquilerRaw(parseFloat(total) || 0);
        setTotalAlquiler(total); // Mantenemos el valor sin formato para la entrada del usuario.
    };

    const handleAbonoChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const abono = e.target.value.replace(/\D/g, '');
        setAbonoRaw(parseFloat(abono) || 0);
        setAbono(abono); // Mantenemos el valor sin formato para la entrada del usuario.
    };

    const handleDepositoChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const deposito = e.target.value.replace(/\D/g, '');
        setDepositoRaw(parseFloat(deposito) || 0);
        setDeposito(deposito); // Mantenemos el valor sin formato para la entrada del usuario.
    };

    const handleTotalAlquilerBlur = () => {
        setTotalAlquiler(formatCurrency(totalAlquilerRaw));
        calcularSaldoRestante();
    };

    const handleAbonoBlur = () => {
        if (abonoRaw > totalAlquilerRaw) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'El abono no puede ser mayor que el total del alquiler.'
            });
            setAbonoRaw(0);
            setAbono('');
        } else {
            setAbono(formatCurrency(abonoRaw));
        }
        calcularSaldoRestante();
    };

    const handleDepositoBlur = () => {
        setDeposito(formatCurrency(depositoRaw));
    };

    const calcularSaldoRestante = () => {
        if (abonoRaw <= totalAlquilerRaw) {
            const saldo = totalAlquilerRaw - abonoRaw;
            setSaldoRestante(formatCurrency(saldo));
        } else {
            setSaldoRestante(formatCurrency(totalAlquilerRaw));
        }
    };

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const formatDateComponents = (date: any) => {
            if (!date) return { year: null, month: null, day: null };

            const d = new Date(date);
            const year: number = d.getFullYear();
            const month = `0${d.getMonth() + 1}`.slice(-2);
            const day = `0${d.getDate()}`.slice(-2);

            return { year, month, day };
        };

        const { year: añoCitaMedidas, month: mesCitaMedidas, day: diaCitaMedidas } = formatDateComponents(calendarValue1);
        const { year: añoEntrega, month: mesEntrega, day: diaEntrega } = formatDateComponents(calendarValue2);
        const formData = {
            nombre: nombre,
            apellido: apellido,
            correo: email,
            celular: phone,
            direccion: direccion,
            idAsesor: idEmpleado,
            idProducto: productoFiltrado?._id,
            identificacion: identificacion,
            sede: sede,
            AñoEntrega: añoEntrega,
            MesEntrega: mesEntrega ? parseInt(mesEntrega, 10) : null,
            DiaEntrega: diaEntrega ? parseInt(diaEntrega, 10) : null,
            NumeroDeFactura: numFactur,
            accesorio: dropdownItem?.name,
            velo: radioValueAcompa,
            aro: radioValue2doAcompa,
            metodoDePago: dropdownItem2?.name,
            Abono: abonoRaw,
            Saldo: totalAlquilerRaw - abonoRaw,
            Deposito: depositoRaw,
            AñoCitaMedidas: añoCitaMedidas,
            MesCitaMedidas: mesCitaMedidas ? parseInt(mesCitaMedidas, 10) : null,
            DiaCitaMedidas: diaCitaMedidas ? parseInt(diaCitaMedidas, 10) : null
        };
        console.log(formData);
        try {
            const response = await postFormulario(formData);
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
                    <h5>Formulario Alquiler</h5>
                    <BreadCrumb home={home} model={breadcrumbItems} />
                </div>
            </div>
            <div className="col-12">
                <div className="card">
                    <h5>Formulario Alquiler Traje o Vestido</h5>
                    <div className="p-fluid formgrid grid">
                        <form className="p-uid formgrid grid" onSubmit={handleSubmit}>
                            <div className="field col-12 md:col-6">
                                <label htmlFor="nombre">Nombre </label>
                                <InputText id="nombre" type="text" value={nombre} onChange={(e) => setNombre(e.target.value)} required />
                            </div>
                            <div className="field col-12 md:col-6">
                                <label htmlFor="apellido">Apellido </label>
                                <InputText id="apellido" type="text" value={apellido} onChange={(e) => setApellido(e.target.value)} required />
                            </div>
                            <div className="field col-12 md:col-6">
                                <label htmlFor="correoElectronico">Correo Electronico</label>
                                <InputText id="correoElectronico" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
                            </div>
                            <div className="field col-12 md:col-3">
                                <label htmlFor="identificacion">Identificacion</label>
                                <InputText id="identificacion" type="text" value={identificacion} onChange={(e) => setIdentificacion(e.target.value)} required />
                            </div>
                            <div className="field col-12 md:col-3">
                                <label htmlFor="phone">Celular</label>
                                <InputText id="phone" type="text" value={phone} onChange={(e) => setPhone(e.target.value)} required />{' '}
                            </div>
                            <div className="field col-12 md:col-6">
                                <label htmlFor="Direccion">Direccion</label>
                                <InputText id="Direccion" type="text" value={direccion} onChange={(e) => setDireccion(e.target.value)} required />
                            </div>
                            <div className="field col-12 md:col-6">
                                <label htmlFor="numFactur">Numero Factura</label>
                                <InputText id="numFactur" type="text" value={numFactur} onChange={(e) => setNumFactur(e.target.value)} required />
                            </div>
                            <div className="field col-12 md:col-6">
                                <h5>Fecha Cita Medidas</h5>
                                <Calendar showIcon showButtonBar value={calendarValue1} onChange={(e) => setCalendarValue1(e.value ?? null)} />
                            </div>
                            <div className="field col-12 md:col-6">
                                <h5>Fecha Entrega</h5>
                                <Calendar showIcon showButtonBar value={calendarValue2} onChange={(e) => setCalendarValue2(e.value ?? null)} />
                            </div>
                            <div className="field col-12 md:col-6">
                                <label htmlFor="refVestido">Referencia Vestido o Traje</label>
                                <InputText id="refVestido" type="text" value={referencia} onChange={handleReferenciaChange} required />
                            </div>
                            <div className="field col-12 md:col-6">
                                <label htmlFor="categoria">Categoría</label>
                                <InputText id="categoria" type="text" value={productoFiltrado?.nombre || 'No se encontro'} readOnly />
                            </div>
                            <div className="field col-12 md:col-6">
                                <label htmlFor="idVesti">Color</label>
                                <InputText id="text" type="text" value={productoFiltrado?.color || ''} readOnly />
                            </div>
                            <div className="field col-12 md:col-6">
                                <label htmlFor="Accesory">Accesorio</label>
                                <Dropdown id="Accesory" value={dropdownItem} onChange={(e) => setDropdownItem(e.value)} options={dropdownItems} optionLabel="name" placeholder="Selecciona uno"></Dropdown>
                            </div>
                            <div className="field col-12 md:col-6">
                                <h5>Acompañante</h5>
                                <div className="grid">
                                    <div className="col-12 md:col-4">
                                        <div className="field-radiobutton">
                                            <RadioButton inputId="option1" name="option" value="Velo" checked={radioValueAcompa === 'Velo'} onChange={(e) => setRadioValueAcompa(e.value)} />
                                            <label htmlFor="option1">Velo</label>
                                        </div>
                                    </div>
                                    <div className="col-12 md:col-4">
                                        <div className="field-radiobutton">
                                            <RadioButton inputId="option2" name="option" value="Mantilla" checked={radioValueAcompa === 'Mantilla'} onChange={(e) => setRadioValueAcompa(e.value)} />
                                            <label htmlFor="option2">Mantilla</label>
                                        </div>
                                    </div>
                                    <div className="col-12 md:col-4">
                                        <div className="field-radiobutton">
                                            <RadioButton inputId="option3" name="option" value="NoAcompa" checked={radioValueAcompa === 'NoAcompa'} onChange={(e) => setRadioValueAcompa(e.value)} />
                                            <label htmlFor="option3">No Acompañante</label>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div className="field col-12 md:col-6">
                                <h5>2do Acompañante</h5>
                                <div className="grid">
                                    <div className="col-12 md:col-4">
                                        <div className="field-radiobutton">
                                            <RadioButton inputId="option4" name="option" value="Aro" checked={radioValue2doAcompa === 'Aro'} onChange={(e) => setRadioValue2doAcompa(e.value)} />
                                            <label htmlFor="option4">Aro</label>
                                        </div>
                                    </div>
                                    <div className="col-12 md:col-4">
                                        <div className="field-radiobutton">
                                            <RadioButton inputId="option5" name="option" value="Gitana" checked={radioValue2doAcompa === 'Gitana'} onChange={(e) => setRadioValue2doAcompa(e.value)} />
                                            <label htmlFor="option5">Gitana</label>
                                        </div>
                                    </div>
                                    <div className="col-12 md:col-4">
                                        <div className="field-radiobutton">
                                            <RadioButton inputId="option6" name="option" value="NoAcompa" checked={radioValue2doAcompa === 'NoAcompa'} onChange={(e) => setRadioValue2doAcompa(e.value)} />
                                            <label htmlFor="option6">No Acompañante</label>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div className="field col-12 md:col-6">
                                <label htmlFor="metpay">Metodo de Pago</label>
                                <Dropdown id="metpay" value={dropdownItem2} onChange={(e) => setDropdownItem2(e.value)} options={dropdownItems2} optionLabel="name" placeholder="Selecciona uno"></Dropdown>
                            </div>
                            <div className="field col-12 md:col-6">
                                <label htmlFor="totalAlquiler">Total Alquiler</label>
                                <InputText id="totalAlquiler" value={totalAlquiler} onChange={handleTotalAlquilerChange} onBlur={handleTotalAlquilerBlur} />
                            </div>
                            <div className="field col-12 md:col-6">
                                <label htmlFor="abono">Abono</label>
                                <InputText id="abono" value={abono} onChange={handleAbonoChange} onBlur={handleAbonoBlur} />
                            </div>
                            <div className="field col-12 md:col-3">
                                <label htmlFor="saldoRestante">Saldo Restante</label>
                                <InputText id="saldoRestante" value={saldoRestante} disabled={true} />
                            </div>
                            <div className="field col-12 md:col-3">
                                <label htmlFor="Deposito">Deposito</label>
                                <InputText id="Deposito" value={deposito} onChange={handleDepositoChange} onBlur={handleDepositoBlur} />
                            </div>
                            <div className="field col-12 md:col-6">
                                <label htmlFor="idAsesorComer">Id Asesora Comercial</label>
                                <InputText id="idAsesorComer" type="text" value={idAsesor} disabled={true} />
                            </div>
                            <div className="field col-12 md:col-6">
                                <label htmlFor="idNombreAsesor">Nombre Asesor@</label>
                                <InputText id="idNombreAsesor" type="text" value={nombreAsesor} disabled={true} />
                            </div>
                            <div className="field col-12 md:col-6">
                                <h5>Aceptas Terminos y Condiciones</h5>
                                <div className="grid termCondition">
                                    <div className="col-12 md:col-3">
                                        <div className="field-checkbox">
                                            <Checkbox inputId="terminosSi" name="terminos" value="Si" checked={checkboxValue.includes('Si')} onChange={onCheckboxChange} />
                                            <label htmlFor="terminosSi">Si</label>
                                        </div>
                                    </div>
                                    <div className="col-12 md:col-3">
                                        <div className="field-checkbox">
                                            <Checkbox inputId="terminosNo" name="terminos" value="No" checked={checkboxValue.includes('No')} onChange={onCheckboxChange} />
                                            <label htmlFor="terminosNo">No</label>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div className="field col-12 md:col-6 containerbutton">
                                <div className="field col-12 md:col-4 buttonform">
                                    <Button label="Aceptar" type="submit"></Button>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Alquiler;
