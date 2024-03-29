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
import { getProducts, postMakeupCreate } from '../../../api/formServices';
import Swal from 'sweetalert2';
import { cookies } from 'next/dist/client/components/headers';
import { getAllEmployees } from '../../../api/taskService';
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

const MakeUpForm = () => {
    const home: MenuItem = { icon: 'pi pi-home', url: '/' };
    const breadcrumbItems: MenuItem[] = [{ label: 'Formularios' }, { label: 'Cita Primera vez' }];
    const [calendarValue4, setCalendarValue4] = useState<string | Date | Date[] | null>(null);
    const [checkboxValue, setCheckboxValue] = useState<string[]>([]);
    const idrol = Cookies.get('idRol');

    // Estados para los productos a usar

    const [productos, setProductos] = useState<Producto[]>([]);
    const [productoFiltrado, setProductoFiltrado] = useState<Producto | null>(null);
    const [productoId, setProductoId] = useState<Producto | null>(null);
    const [debouncedRef, setDebouncedRef] = useState('');

    // Value to sent
    const [nombre, setNombre] = useState('');
    const [apellido, setApellido] = useState('');
    const [identificacion, setIdentificacion] = useState('');
    const [phone, setPhone] = useState('');
    const [direccion, setDireccion] = useState('');
    const [email, setEmail] = useState('');
    const [referencia, setReferencia] = useState('');
    const [horaCita, setHoraCita] = useState(null);
    const [numFactu, setNumfactu] = useState('');

    const [calendarValue1, setCalendarValue1] = useState<string | Date | Date[] | null>(null);
    const [calendarValue2, setCalendarValue2] = useState<string | Date | Date[] | null>(null);
    const [dropdownItem, setDropdownItem] = useState<DropdownItem | null>(null);
    const [dropdownItem2, setDropdownItem2] = useState<DropdownItem | null>(null);

    const [employees, setEmployees] = useState([]);
    const [selectedEmployee, setSelectedEmployee] = useState(null);
    const [employeeOptions, setEmployeeOptions] = useState([]);

    useEffect(() => {
        const fetchAllEmployees = async () => {
            try {
                const allEmployees = await getAllEmployees();
                const filteredEmployees = allEmployees.filter((employee) => employee.usuario.rol._id === rolId['maquilladora']);
                const mappedOptions = filteredEmployees.map((employee) => ({
                    name: employee.usuario.nombreApellido,
                    code: employee.usuario._id
                }));
                setEmployeeOptions(mappedOptions);
            } catch (error) {
                console.error('Error al cargar empleados:', error);
            }
        };

        fetchAllEmployees();
    }, []);

    // const userFilterByMakeup = () => {
    //     const filteredEmployees = employees.filter((employee) => employee.usuario.rol._id === rolId['maquilladora']);

    //     const employeeOptions = filteredEmployees.map((employee) => ({
    //         text: employee.usuario.nombreApellido,
    //         value: employee.id.toString()
    //     }));
    // };

    const rolId = {
        modista: '64a780574f5c1f4272d8e66c',
        lavanderia: '64c99d28bf3ae63b80f936e3',
        maquilladora: '653ea80670556042587486bd'
    };

    //Informacion Asesor
    const idAsesor = Cookies.get('userId');
    const nombreAsesor = Cookies.get('nombreApellido');
    const idEmpleado = Cookies.get('idEmpleado');
    const dropdownItems: DropdownItem[] = useMemo(
        () => [
            { name: 'Boda', code: 'Boda' },
            { name: 'Social', code: 'Social' },
            { name: 'Social-2', code: 'Social-2' },
            { name: 'XV', code: 'XV' },
            { name: 'Plan Oro', code: 'Plan Oro' },
            { name: 'Make Up Social', code: 'Make Up Social' },
            { name: 'Novia', code: 'Novia' },
            { name: 'Novia-Oro', code: 'Novia-Oro' }
        ],
        []
    );

    useEffect(() => {
        setDropdownItem(dropdownItems[0]);
    }, [dropdownItems]);

    // useEffect(() => {
    //     const timerId = setTimeout(() => {
    //         setDebouncedRef(referencia);
    //     }, 500);
    //     return () => {
    //         clearTimeout(timerId);
    //     };
    // }, [referencia]);

    const handleReferenciaChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setReferencia(e.target.value.trim());
    };

    const dropdownItems2: DropdownItem[] = useMemo(
        () => [
            { name: 'AMBAR', code: 'AMBAR' },
            { name: 'DOMICILIO', code: 'DOMICILIO' }
        ],
        []
    );

    useEffect(() => {
        setDropdownItem2(dropdownItems2[0]);
    }, [dropdownItems2]);

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

    const formatTimeComponents = (time: any) => {
        if (!time) return { hora: null, minuto: null };

        const t = new Date(time);
        const hora: number = t.getHours();
        const minuto: number = t.getMinutes();

        return { hora, minuto };
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
        const { hora, minuto } = formatTimeComponents(horaCita);

        const formData = {
            cliente: nombre + ' ' + apellido,
            //numeroCliente: phone,
            //correoCliente: email,
            entrega: dropdownItem2.name,
            maquilladora: selectedEmployee,
            tipo: dropdownItem.name,
            dia: diaCitaMedidas ? parseInt(diaCitaMedidas, 10) : null,
            mes: mesCitaMedidas ? parseInt(mesCitaMedidas, 10) : null,
            año: añoCitaMedidas,
            hora: hora,
            minutos: minuto,
            numeroFactura: numFactu,
            referencia: referencia,
            direccion: direccion
        };
        console.log(formData);
        try {
            const response = await postMakeupCreate(formData);
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
                    <h5>Formulario Para Make-up</h5>
                    <BreadCrumb home={home} model={breadcrumbItems} />
                </div>
            </div>
            <div className="col-12">
                <div className="card">
                    <h5>Formulario Para Make-up</h5>
                    <div className="p-fluid formgrid grid">
                        <form className="p-uid formgrid grid" onSubmit={handleSubmit}>
                            <div className="field col-12 md:col-6">
                                <label htmlFor="nombre">Nombre </label>
                                <InputText id="nombre" type="text" value={nombre} onChange={(e) => setNombre(e.target.value)} required />
                            </div>
                            <div className="field col-12 md:col-3">
                                <label htmlFor="apellido">Apellido </label>
                                <InputText id="apellido" type="text" value={apellido} onChange={(e) => setApellido(e.target.value)} required />
                            </div>
                            <div className="field col-12 md:col-3">
                                <label htmlFor="factura">Numero Factura </label>
                                <InputText id="factura" type="text" value={numFactu} onChange={(e) => setNumfactu(e.target.value)} required />
                            </div>
                            {/*<div className="field col-12 md:col-6">
                                <label htmlFor="correoElectronico">Correo Electronico</label>
                                <InputText id="correoElectronico" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
    </div>*/}
                            {/* <div className="field col-12 md:col-3">
                                <label htmlFor="identificacion">Identificacion</label>
                                <InputText id="identificacion" type="text" value={identificacion} onChange={(e) => setIdentificacion(e.target.value)} required />
</div>*/}
                            <div className="field col-12 md:col-3">
                                <label htmlFor="phone">Celular</label>
                                <InputText id="phone" type="text" value={phone} onChange={(e) => setPhone(e.target.value)} required />{' '}
                            </div>
                            <div className="field col-12 md:col-3">
                                <label htmlFor="Direccion">Direccion</label>
                                <InputText id="Direccion" type="text" value={direccion} onChange={(e) => setDireccion(e.target.value)} required />
                            </div>
                            <div className="field col-12 md:col-3">
                                <label htmlFor="Accesory">Tipo</label>
                                <Dropdown id="Accesory" value={dropdownItem} onChange={(e) => setDropdownItem(e.value)} options={dropdownItems} optionLabel="name" placeholder="Selecciona uno"></Dropdown>
                            </div>
                            <div className="field col-12 md:col-3">
                                <label htmlFor="delivery">Entrega</label>
                                <Dropdown id="delivery" value={dropdownItem2} onChange={(e) => setDropdownItem2(e.value)} options={dropdownItems2} optionLabel="name" placeholder="Selecciona uno"></Dropdown>
                            </div>
                            <div className="field col-12 md:col-3">
                                <label htmlFor="refVestido">Referencia Vestido o Traje</label>
                                <InputText id="refVestido" type="text" value={referencia} onChange={handleReferenciaChange} required />
                            </div>
                            <div className="field col-12 md:col-3">
                                <label htmlFor="categoria">Categoría</label>
                                <InputText id="categoria" type="text" value={productoFiltrado?.nombre || 'No se encontro'} readOnly />
                            </div>
                            <div className="field col-12 md:col-6">
                                <label htmlFor="employeeDropdown">Empleado</label>
                                <Dropdown id="employeeDropdown" value={selectedEmployee} options={employeeOptions} onChange={(e) => setSelectedEmployee(e.value)} optionLabel="name" placeholder="Selecciona un empleado" optionValue="code" />
                            </div>
                            <div className="field col-12 md:col-6">
                                <h5>Fecha Makeup </h5>
                                <Calendar showIcon showButtonBar value={calendarValue1} onChange={(e) => setCalendarValue1(e.value ?? null)} />
                            </div>
                            <div className="field col-12 md:col-6">
                                <h5>Hora Makeup </h5>
                                <Calendar id="horaCita" value={horaCita} onChange={(e) => setHoraCita(e.value)} showTime timeOnly hourFormat="24" showIcon />
                            </div>

                            {/*<div className="field col-12 md:col-6">
                                <label htmlFor="idAsesorComer">Id Asesora Comercial</label>
                                <InputText id="idAsesorComer" type="text" value={idAsesor} disabled={true} />
                            </div>
                            <div className="field col-12 md:col-6">
                                <label htmlFor="idNombreAsesor">Nombre Asesor@</label>
                                <InputText id="idNombreAsesor" type="text" value={nombreAsesor} disabled={true} />
</div>*/}
                            <div className="field col-12 md:col-6 mb-0 pb-0 pt-[1rem]containerbutton">
                                <div className="field col-12 md:col-4 md:mb-0       buttonform">
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

export default MakeUpForm;
