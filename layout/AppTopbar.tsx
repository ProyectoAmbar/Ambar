/* eslint-disable @next/next/no-img-element */

import Link from 'next/link';
import { classNames } from 'primereact/utils';
import React, { forwardRef, useContext, useImperativeHandle, useRef } from 'react';
import { AppTopbarRef } from '../types/types';
import Cookies from 'js-cookie';
import { LayoutContext } from './context/layoutcontext';
import { Menu } from 'primereact/menu';
import { Button } from 'primereact/button';
import Swal from 'sweetalert2'; // Importa SweetAlert2

const AppTopbar = forwardRef<AppTopbarRef>((props, ref) => {
    const { layoutConfig, layoutState, onMenuToggle, showProfileSidebar } = useContext(LayoutContext);
    const menubuttonRef = useRef(null);
    const topbarmenuRef = useRef(null);
    const topbarmenubuttonRef = useRef(null);
    const menu = useRef<Menu>(null);

    const showMenu = (event: React.MouseEvent<HTMLButtonElement>) => {
        if (menu.current) {
            menu.current.toggle(event);
        }
    };

    const handleSignOut = () => {
        Swal.fire({
            title: '¿Estás seguro?',
            text: 'Vas a cerrar sesión',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Sí, cerrar sesión'
        }).then((result) => {
            if (result.isConfirmed) {
                Cookies.remove('idEmpleado');
                Cookies.remove('rolName');
                Cookies.remove('nombreApellido');
                Cookies.remove('idRol');
                Cookies.remove('correo');
                Cookies.remove('Token');
                Cookies.remove('userId');
                Cookies.remove('IdTareaModista');
                Cookies.remove('IdCitaMedidas');
                Cookies.remove('IdTareaLavanderia');

                
                

                window.location.href = '/auth/login';
            }
        });
    };

    const items = [
        { label: 'Profile', icon: 'pi pi-fw pi-user' },
        { label: 'Settings', icon: 'pi pi-fw pi-cog' },
        { separator: true },
        {
            label: 'Salir',
            icon: 'pi pi-fw pi-sign-out',
            command: () => handleSignOut()
        }
    ];
    useImperativeHandle(ref, () => ({
        menubutton: menubuttonRef.current,
        topbarmenu: topbarmenuRef.current,
        topbarmenubutton: topbarmenubuttonRef.current
    }));
    {
        /* Barra de informacion superior */
    }
    return (
        <div className="layout-topbar">
            <Link href="/" className="layout-topbar-logo">
                {/*              <img src={`/layout/images/logo-${layoutConfig.colorScheme !== 'light' ? 'white' : 'dark'}.svg`} width="47.22px" height={'35px'} alt="logo" />
                 */}{' '}
                <span>Ambar</span>
            </Link>

            <button ref={menubuttonRef} type="button" className="p-link layout-menu-button layout-topbar-button" onClick={onMenuToggle}>
                <i className="pi pi-bars" />
            </button>

            <button ref={topbarmenubuttonRef} type="button" className="p-link layout-topbar-menu-button layout-topbar-button" onClick={showProfileSidebar}>
                <i className="pi pi-ellipsis-v" />
            </button>

            <div ref={topbarmenuRef} className={classNames('layout-topbar-menu', { 'layout-topbar-menu-mobile-active': layoutState.profileSidebarVisible })}>
                <button type="button" className="p-link layout-topbar-button">
                    <i className="pi pi-calendar"></i>
                    <span>Calendario</span>
                </button>
                <button type="button" className="p-link layout-topbar-button" onClick={showMenu}>
                    <i className="pi pi-user"></i>
                    <span>Perfil</span>
                </button>

                <Menu model={items} popup ref={menu} id="overlay_menu" />
                {/* <Link href="/documentation">
                    <button type="button" className="p-link layout-topbar-button">
                        <i className="pi pi-cog"></i>
                        <span>Configuracion</span>
                    </button>
</Link>*/}
            </div>
        </div>
    );
});

AppTopbar.displayName = 'AppTopbar';

export default AppTopbar;
