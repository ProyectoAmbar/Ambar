import React, { useEffect, useState, FC, useContext } from 'react';
import { toast } from 'react-toastify';
import axios from 'axios';
import Cookies from 'js-cookie';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { Password } from 'primereact/password';
import { LayoutContext } from '../../../../layout/context/layoutcontext';
import { InputText } from 'primereact/inputtext';
import { classNames } from 'primereact/utils';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Swal from 'sweetalert2';
import { login, getUserInfo } from '../../../api/authServices';
import { getWorkersId } from '../../../api/authServices';

const ClientLogin: FC = () => {
    const [correo, setCorreo] = useState('');
    const [password, setPassword] = useState('');
    const [ShowPassword, setShowPassword] = useState(false);
    const [checked, setChecked] = useState(false);
    const { layoutConfig } = useContext(LayoutContext);
    const [redirectToHome, setRedirectToHome] = useState(false);
    const islogin = 'true';
    const handleShowPassword = () => {
        setShowPassword(!ShowPassword);
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if ([correo, password].includes('')) {
            toast.error('Todos los campos son obligatorios', { theme: 'light' });
            return;
        }

        if (password.length < 6) {
            toast.error('La contraseña debe Contener al menos 6 Caracteres', { theme: 'light' });
            return;
        }

        try {
            const apiResponse = await login(correo, password);

            if (apiResponse && apiResponse.userId && apiResponse.accesToken && apiResponse.rol) {
                Cookies.set('userId', apiResponse.userId);
                Cookies.set('Token', apiResponse.accesToken);
                Cookies.set('idRol', apiResponse.rol);

                const userResponse = await getUserInfo(apiResponse.userId);

                if (userResponse) {
                    Cookies.set('nombreApellido', userResponse.nombreApellido);
                    Cookies.set('correo', userResponse.correo);
                    Cookies.set('rolName', userResponse.rol.name);
                }
                const idrol = Cookies.get('idRol');
                const idAsesor = Cookies.get('userId');

                const nombre = Cookies.get('nombreApellido');
                const WorkerdId = await getWorkersId(idAsesor, idrol);
                Cookies.set('idEmpleado', WorkerdId);
                // Cookies.set('Login', islogin);
                Swal.fire({
                    icon: 'success',
                    title: 'Inicio de sesión exitoso',
                    text: `Bienvenido ${nombre}!`
                }).then(() => {
                    setTimeout(() => {
                        setRedirectToHome(true);
                    }, 1000);
                });
                setRedirectToHome(true);
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Login fallido. Revisar Credenciales.'
                });
            }
        } catch (error) {
            console.error(error);
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Ocurrió un error, intente nuevamente.'
            });
        }
    };

    useEffect(() => {
        if (redirectToHome && typeof window !== 'undefined') {
            window.location.href = '/';
        }
    }, [redirectToHome]);

    const containerClassName = classNames('surface-ground flex align-items-center justify-content-center min-h-screen min-w-screen overflow-hidden', { 'p-input-filled': layoutConfig.inputStyle === 'filled' });

    return (
        <div className={containerClassName}>
            <div className="flex flex-column align-items-center justify-content-center">
                <div
                    style={{
                        borderRadius: '56px',
                        padding: '0.3rem',
                        background: 'linear-gradient(90deg, var(--primary-color) 10%, rgba(33, 150, 243, 0) 30%)',
                        animation: 'movingGradient 4s infinite'
                    }}
                >
                    <div className="w-full surface-card py-7 px-6 sm:px-8" style={{ borderRadius: '53px' }}>
                        <div className="text-center mb-5">
                            <img src="/demo/images/login/loginImage.jpg" alt="Image" height="50" className="mb-3" />
                            <div className="text-900 text-3xl font-medium mb-3">Bienvenido, Ambar Couture!</div>
                            <span className="text-600 font-medium">Inicia Sesión para continuar</span>
                        </div>

                        <form onSubmit={handleSubmit}>
                            <label htmlFor="email1" className="block text-900 text-xl font-medium mb-2">
                                Correo Electronico
                            </label>
                            <InputText id="email1" type="text" placeholder="Correo Electronico" value={correo} onChange={(e) => setCorreo(e.target.value)} className="w-full md:w-30rem mb-5" style={{ padding: '1rem' }} />

                            <label htmlFor="password1" className="block text-900 font-medium text-xl mb-2">
                                Contraseña
                            </label>
                            <Password
                                inputId="password1"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="Contraseña"
                                toggleMask={ShowPassword}
                                className="w-full mb-5"
                                inputClassName="w-full p-3 md:w-30rem"
                                weakLabel="Débil"
                                mediumLabel="Medio"
                                strongLabel="Fuerte"
                                promptLabel="Ingresa una contraseña"
                            />

                            <div className="flex align-items-center justify-content-between mb-5 gap-5">
                                <div className="flex align-items-center">
                                    <Checkbox inputId="rememberme1" checked={checked} onChange={(e) => setChecked(e.checked ?? false)} className="mr-2"></Checkbox>
                                    <label htmlFor="rememberme1">Recuerdame</label>
                                </div>
                                <a className="font-medium no-underline ml-2 text-right cursor-pointer" style={{ color: 'var(--primary-color)' }}>
                                    Olvidaste Contraseña?
                                </a>
                            </div>
                            <Button label="Iniciar Sesión" className="w-full p-3 text-xl" type="submit"></Button>
                        </form>
                    </div>
                </div>
            </div>
            <ToastContainer />
        </div>
    );
};

export default ClientLogin;
