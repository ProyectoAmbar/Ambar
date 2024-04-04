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
import { getProducts, postCitaPrimeraVez } from '../../../api/formServices';
import Swal from 'sweetalert2';
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

const CitaPrimera = () => {
    const home: MenuItem = { icon: 'pi pi-home', url: '/' };
    const breadcrumbItems: MenuItem[] = [{ label: 'Formularios' }, { label: 'Cita Primera vez' }];
    const [calendarValue4, setCalendarValue4] = useState<string | Date | Date[] | null>(null);
    const [checkboxValue, setCheckboxValue] = useState<string[]>([]);
    const idrol = Cookies.get('idRol');
    // Estados para los productos a usar

    const [abonoRaw, setAbonoRaw] = useState(0);
    const [depositoRaw, setDepositoRaw] = useState(0);

    // Value to sent
    const [nombre, setNombre] = useState('');
    const [apellido, setApellido] = useState('');
    const [identificacion, setIdentificacion] = useState('');
    const [phone, setPhone] = useState('');
    const [direccion, setDireccion] = useState('');
    const [email, setEmail] = useState('');
    const [referencia, setReferencia] = useState('');
    const sede: string = 'villavicencio';
    const [horaCita, setHoraCita] = useState(null);

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
            { name: 'Alquiler', code: 'alquiler' },
            { name: 'Make-up', code: 'maleup' },
            { name: 'Sesion De Fotos', code: 'sesionFotos' },
            { name: 'Foto-Make-uP', code: 'FotoMake' },
            { name: 'Novia', code: 'novia' },
            { name: 'Traje', code: 'traje' },
            { name: 'Gala', code: 'Gala' },
            { name: 'Traje', code: 'traje' },
            { name: 'Quince años', code: 'Quince-años' },
            { name: 'Primera comunion', code: 'Primera-Comunion' }
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
            nombre: nombre,
            apellido: apellido,
            //correo: email,
            direccion: direccion,
            telefono: phone,
            motivo: dropdownItem?.name,
            año: añoCitaMedidas,
            mes: mesCitaMedidas ? parseInt(mesCitaMedidas, 10) : null,
            dia: diaCitaMedidas ? parseInt(diaCitaMedidas, 10) : null,
            hora: hora,
            minuto: minuto
        };
        console.log(formData);
        try {
            const response = await postCitaPrimeraVez(formData);
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
                    <h5>Formulario Cita Primera Vez</h5>
                    <BreadCrumb home={home} model={breadcrumbItems} />
                </div>
            </div>
            <div className="col-12">
                <div className="card">
                    <h5>Formulario Para Cita</h5>
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
                            <div className="field col-12 md:col-6">
                                <label htmlFor="Accesory">Motivo Cita</label>
                                <Dropdown id="Accesory" value={dropdownItem} onChange={(e) => setDropdownItem(e.value)} options={dropdownItems} optionLabel="name" placeholder="Selecciona uno"></Dropdown>
                            </div>
                            <div className="field col-12 md:col-6">
                                <h5>Fecha Cita </h5>
                                <Calendar showIcon showButtonBar value={calendarValue1} onChange={(e) => setCalendarValue1(e.value ?? null)} />
                            </div>
                            <div className="field col-12 md:col-6">
                                <h5>Hora Cita </h5>
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

export default CitaPrimera;
