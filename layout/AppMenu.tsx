/* eslint-disable @next/next/no-img-element */
/* Menu sidebar y sus rutas */
import React, { useContext, useState, useEffect } from 'react';
import AppMenuitem from './AppMenuitem';
import { LayoutContext } from './context/layoutcontext';
import { MenuProvider } from './context/menucontext';
import Link from 'next/link';
import { AppMenuItem } from '../types/types';
import Cookies from 'js-cookie';
const AppMenu = () => {
    const { layoutConfig } = useContext(LayoutContext);
    const [filteredModel, setFilteredModel] = useState<AppMenuItem[]>([]);

    // const model: AppMenuItem[] = [
    //     {
    //         label: 'Inicio',
    //         items: [{ label: 'Principal', icon: 'pi pi-fw pi-home', to: '/' }]
    //     },
    //     {
    //         label: 'Mas Paginas ',
    //         items: [
    //             { label: 'Formulario Alquiler', icon: 'pi pi-fw pi-pencil', to: '/pages/formsAlquiler' },
    //             { label: 'Formulario Cita primera vez', icon: 'pi pi-fw pi-pencil', to: '/pages/formsCitaPrimera' },
    //             { label: 'Formulario Medidas', icon: 'pi pi-fw pi-pencil', to: '/pages/formsMedidas' },
    //             { label: 'Formulario Sastreria', icon: 'pi pi-fw pi-pencil', to: '/pages/formsSastreria' },
    //             { label: 'Formulario Lavanderia', icon: 'pi pi-fw pi-pencil', to: '/pages/formsLavanderia' },
    //             { label: 'Formulario Makeup', icon: 'pi pi-fw pi-pencil', to: '/pages/FormMakeup' },
    //             { label: 'Formulario Sesion de Fotos', icon: 'pi pi-fw pi-pencil', to: '/pages/FormPhoto' },
    //             { label: 'Ver Tareas', icon: 'pi pi-fw pi-eye', to: '/pages/RolViewTask' },
    //             { label: 'Ver Citas Primera Vez', icon: 'pi pi-fw pi-eye', to: '/pages/CitaPrimeraRespond' },
    //             { label: 'Ver Sesion de Fotos', icon: 'pi pi-fw pi-eye', to: '/pages/fotosRespond' },
    //             { label: 'Calendario', icon: 'pi pi-fw pi-calendar', to: '/pages/CalendarTask' },
    //             // { label: 'Formulario Consult', icon: 'pi pi-fw pi-id-card', to: '/Consult' },
    //             { label: 'Ingresos y Egresos', icon: 'pi pi-fw pi-money-bill', to: '/pages/Ingresos' },
    //             // { label: 'Form Layout', icon: 'pi pi-fw pi-id-card', to: '/uikit/formlayout' },
    //             { label: 'Usuarios', icon: 'pi pi-fw pi-user', to: '/pages/usersAllFolder' },
    //             { label: 'Asignar Tareas', icon: 'pi pi-fw pi-id-card', to: '/pages/assignmentview' },
    //             { label: 'Ver Entregas y Devoluciones', icon: 'pi pi-fw pi-eye ', to: '/pages/EntregarDevolver' },
    //             { label: 'Productos', icon: 'pi pi-fw pi-shopping-bag', to: '/pages/crud' },
    //             { label: 'Mirar Tareas', icon: 'pi pi-fw pi-eye', to: '/pages/taskview' },
    //             // { label: 'Input', icon: 'pi pi-fw pi-check-square', to: '/uikit/input' },
    //             // { label: 'Float Label', icon: 'pi pi-fw pi-bookmark', to: '/uikit/floatlabel' },
    //             // { label: 'Invalid State', icon: 'pi pi-fw pi-exclamation-circle', to: '/uikit/invalidstate' },
    //             // { label: 'Button', icon: 'pi pi-fw pi-mobile', to: '/uikit/button', class: 'rotated-icon' },
    //             // { label: 'Table', icon: 'pi pi-fw pi-table', to: '/uikit/table' },
    //             // { label: 'List', icon: 'pi pi-fw pi-list', to: '/uikit/list' },
    //             // { label: 'Tree', icon: 'pi pi-fw pi-share-alt', to: '/uikit/tree' },
    //             // { label: 'Panel', icon: 'pi pi-fw pi-tablet', to: '/uikit/panel' },
    //             // { label: 'Overlay', icon: 'pi pi-fw pi-clone', to: '/uikit/overlay' },
    //             // { label: 'Media', icon: 'pi pi-fw pi-image', to: '/uikit/media' },
    //             // { label: 'Menu', icon: 'pi pi-fw pi-bars', to: '/uikit/menu', preventExact: true },
    //             // { label: 'Message', icon: 'pi pi-fw pi-comment', to: '/uikit/message' },
    //             // { label: 'File', icon: 'pi pi-fw pi-file', to: '/uikit/file' },
    //             // { label: 'Chart', icon: 'pi pi-fw pi-chart-bar', to: '/uikit/charts' },
    //             // { label: 'Misc', icon: 'pi pi-fw pi-circle', to: '/uikit/misc' }
    //         ]
    //     },
    //     // {
    //     //     label: 'Prime Blocks',
    //     //     items: [
    //     //         { label: 'Free Blocks', icon: 'pi pi-fw pi-eye', to: '/blocks', badge: 'NEW' },
    //     //         { label: 'All Blocks', icon: 'pi pi-fw pi-globe', url: 'https://blocks.primereact.org', target: '_blank' }
    //     //     ]
    //     // },
    //     // {
    //     //     label: 'Utilities',
    //     //     items: [
    //     //         { label: 'PrimeIcons', icon: 'pi pi-fw pi-prime', to: '/utilities/icons' },
    //     //         { label: 'PrimeFlex', icon: 'pi pi-fw pi-desktop', url: 'https://primeflex.org/', target: '_blank' }
    //     //     ]
    //     // },
    //     // {
    //     //     label: 'Pages',
    //     //     icon: 'pi pi-fw pi-briefcase',
    //     //     to: '/pages',
    //     //     items: [
    //     //         {
    //     //             label: 'Landing',
    //     //             icon: 'pi pi-fw pi-globe',
    //     //             to: '/landing'
    //     //         },
    //     //         {
    //     //             label: 'Auth',
    //     //             icon: 'pi pi-fw pi-user',
    //     //             items: [
    //     //                 {
    //     //                     label: 'Login',
    //     //                     icon: 'pi pi-fw pi-sign-in',
    //     //                     to: '/auth/login'
    //     //                 },
    //     //                 {
    //     //                     label: 'Error',
    //     //                     icon: 'pi pi-fw pi-times-circle',
    //     //                     to: '/auth/error'
    //     //                 },
    //     //                 {
    //     //                     label: 'Access Denied',
    //     //                     icon: 'pi pi-fw pi-lock',
    //     //                     to: '/auth/access'
    //     //                 }
    //     //             ]
    //     //         },
    //     //         {
    //     //             label: 'Crud',
    //     //             icon: 'pi pi-fw pi-pencil',
    //     //             to: '/pages/crud'
    //     //         },
    //     //         {
    //     //             label: 'Timeline',
    //     //             icon: 'pi pi-fw pi-calendar',
    //     //             to: '/pages/timeline'
    //     //         },
    //     //         {
    //     //             label: 'Not Found',
    //     //             icon: 'pi pi-fw pi-exclamation-circle',
    //     //             to: '/pages/notfound'
    //     //         },
    //     //         {
    //     //             label: 'Empty',
    //     //             icon: 'pi pi-fw pi-circle-off',
    //     //             to: '/pages/empty'
    //     //         }
    //     //     ]
    //     // },
    //     // {
    //     //     label: 'Hierarchy',
    //     //     items: [
    //     //         {
    //     //             label: 'Submenu 1',
    //     //             icon: 'pi pi-fw pi-bookmark',
    //     //             items: [
    //     //                 {
    //     //                     label: 'Submenu 1.1',
    //     //                     icon: 'pi pi-fw pi-bookmark',
    //     //                     items: [
    //     //                         { label: 'Submenu 1.1.1', icon: 'pi pi-fw pi-bookmark' },
    //     //                         { label: 'Submenu 1.1.2', icon: 'pi pi-fw pi-bookmark' },
    //     //                         { label: 'Submenu 1.1.3', icon: 'pi pi-fw pi-bookmark' }
    //     //                     ]
    //     //                 },
    //     //                 {
    //     //                     label: 'Submenu 1.2',
    //     //                     icon: 'pi pi-fw pi-bookmark',
    //     //                     items: [{ label: 'Submenu 1.2.1', icon: 'pi pi-fw pi-bookmark' }]
    //     //                 }
    //     //             ]
    //     //         },
    //     //         {
    //     //             label: 'Submenu 2',
    //     //             icon: 'pi pi-fw pi-bookmark',
    //     //             items: [
    //     //                 {
    //     //                     label: 'Submenu 2.1',
    //     //                     icon: 'pi pi-fw pi-bookmark',
    //     //                     items: [
    //     //                         { label: 'Submenu 2.1.1', icon: 'pi pi-fw pi-bookmark' },
    //     //                         { label: 'Submenu 2.1.2', icon: 'pi pi-fw pi-bookmark' }
    //     //                     ]
    //     //                 },
    //     //                 {
    //     //                     label: 'Submenu 2.2',
    //     //                     icon: 'pi pi-fw pi-bookmark',
    //     //                     items: [{ label: 'Submenu 2.2.1', icon: 'pi pi-fw pi-bookmark' }]
    //     //                 }
    //     //             ]
    //     //         }
    //     //     ]
    //     // },
    //     // {
    //     //     label: 'Get Started',
    //     //     items: [
    //     //         {
    //     //             label: 'Documentation',
    //     //             icon: 'pi pi-fw pi-question',
    //     //             to: '/documentation'
    //     //         },
    //     //         {
    //     //             label: 'View Source',
    //     //             icon: 'pi pi-fw pi-search',
    //     //             url: 'https://github.com/primefaces/sakai-react',
    //     //             target: '_blank'
    //     //         }
    //     //     ]
    //     // }
    // ];
    useEffect(() => {
        const userRole = Cookies.get('rolName');
        console.log('Rol del usuario:', userRole);
        const model: AppMenuItem[] = [
            {
                label: 'Inicio',
                items: [{ label: 'Principal', icon: 'pi pi-fw pi-home', to: '/' }]
            },
            {
                label: 'Mas Paginas ',
                items: [
                    { label: 'Formulario Alquiler', icon: 'pi pi-fw pi-pencil', to: '/pages/formsAlquiler', roles: ['Admin'] },
                    { label: 'Formulario Cita primera vez', icon: 'pi pi-fw pi-pencil', to: '/pages/formsCitaPrimera' },
                    { label: 'Formulario Medidas', icon: 'pi pi-fw pi-pencil', to: '/pages/formsMedidas', roles: ['Admin'] },
                    { label: 'Formulario Sastreria', icon: 'pi pi-fw pi-pencil', to: '/pages/formsSastreria', roles: ['Admin'] },
                    { label: 'Formulario Lavanderia', icon: 'pi pi-fw pi-pencil', to: '/pages/formsLavanderia', roles: ['Admin'] },
                    { label: 'Formulario Makeup', icon: 'pi pi-fw pi-pencil', to: '/pages/FormMakeup', roles: ['Admin'] },
                    { label: 'Formulario Sesion de Fotos', icon: 'pi pi-fw pi-pencil', to: '/pages/FormPhoto', roles: ['Admin'] },
                    { label: 'Ver Tareas', icon: 'pi pi-fw pi-eye', to: '/pages/RolViewTask' },
                    { label: 'Ver Citas Primera Vez', icon: 'pi pi-fw pi-eye', to: '/pages/CitaPrimeraRespond', roles: ['Admin', 'Asesor'] },
                    { label: 'Ver Sesion de Fotos', icon: 'pi pi-fw pi-eye', to: '/pages/fotosRespond' },
                    { label: 'Calendario', icon: 'pi pi-fw pi-calendar', to: '/pages/CalendarTask' },
                    // { label: 'Formulario Consult', icon: 'pi pi-fw pi-id-card', to: '/Consult' },
                    { label: 'Ingresos y Egresos', icon: 'pi pi-fw pi-money-bill', to: '/pages/Ingresos', roles: ['Admin'] },
                    // { label: 'Form Layout', icon: 'pi pi-fw pi-id-card', to: '/uikit/formlayout' },
                    { label: 'Usuarios', icon: 'pi pi-fw pi-user', to: '/pages/usersAllFolder', roles: ['Admin'] },
                    { label: 'Asignar Tareas', icon: 'pi pi-fw pi-id-card', to: '/pages/assignmentview', roles: ['Admin'] },
                    { label: 'Ver Entregas y Devoluciones', icon: 'pi pi-fw pi-eye ', to: '/pages/EntregarDevolver', roles: ['Admin', 'Asesor'] },
                    { label: 'Productos', icon: 'pi pi-fw pi-shopping-bag', to: '/pages/crud' },
                    { label: 'Mirar Tareas General', icon: 'pi pi-fw pi-eye', to: '/pages/taskview' }
                    // { label: 'Input', icon: 'pi pi-fw pi-check-square', to: '/uikit/input' },
                    // { label: 'Float Label', icon: 'pi pi-fw pi-bookmark', to: '/uikit/floatlabel' },
                    // { label: 'Invalid State', icon: 'pi pi-fw pi-exclamation-circle', to: '/uikit/invalidstate' },
                    // { label: 'Button', icon: 'pi pi-fw pi-mobile', to: '/uikit/button', class: 'rotated-icon' },
                    // { label: 'Table', icon: 'pi pi-fw pi-table', to: '/uikit/table' },
                    // { label: 'List', icon: 'pi pi-fw pi-list', to: '/uikit/list' },
                    // { label: 'Tree', icon: 'pi pi-fw pi-share-alt', to: '/uikit/tree' },
                    // { label: 'Panel', icon: 'pi pi-fw pi-tablet', to: '/uikit/panel' },
                    // { label: 'Overlay', icon: 'pi pi-fw pi-clone', to: '/uikit/overlay' },
                    // { label: 'Media', icon: 'pi pi-fw pi-image', to: '/uikit/media' },
                    // { label: 'Menu', icon: 'pi pi-fw pi-bars', to: '/uikit/menu', preventExact: true },
                    // { label: 'Message', icon: 'pi pi-fw pi-comment', to: '/uikit/message' },
                    // { label: 'File', icon: 'pi pi-fw pi-file', to: '/uikit/file' },
                    // { label: 'Chart', icon: 'pi pi-fw pi-chart-bar', to: '/uikit/charts' },
                    // { label: 'Misc', icon: 'pi pi-fw pi-circle', to: '/uikit/misc' }
                ]
            }
            // {
            //     label: 'Prime Blocks',
            //     items: [
            //         { label: 'Free Blocks', icon: 'pi pi-fw pi-eye', to: '/blocks', badge: 'NEW' },
            //         { label: 'All Blocks', icon: 'pi pi-fw pi-globe', url: 'https://blocks.primereact.org', target: '_blank' }
            //     ]
            // },
            // {
            //     label: 'Utilities',
            //     items: [
            //         { label: 'PrimeIcons', icon: 'pi pi-fw pi-prime', to: '/utilities/icons' },
            //         { label: 'PrimeFlex', icon: 'pi pi-fw pi-desktop', url: 'https://primeflex.org/', target: '_blank' }
            //     ]
            // },
            // {
            //     label: 'Pages',
            //     icon: 'pi pi-fw pi-briefcase',
            //     to: '/pages',
            //     items: [
            //         {
            //             label: 'Landing',
            //             icon: 'pi pi-fw pi-globe',
            //             to: '/landing'
            //         },
            //         {
            //             label: 'Auth',
            //             icon: 'pi pi-fw pi-user',
            //             items: [
            //                 {
            //                     label: 'Login',
            //                     icon: 'pi pi-fw pi-sign-in',
            //                     to: '/auth/login'
            //                 },
            //                 {
            //                     label: 'Error',
            //                     icon: 'pi pi-fw pi-times-circle',
            //                     to: '/auth/error'
            //                 },
            //                 {
            //                     label: 'Access Denied',
            //                     icon: 'pi pi-fw pi-lock',
            //                     to: '/auth/access'
            //                 }
            //             ]
            //         },
            //         {
            //             label: 'Crud',
            //             icon: 'pi pi-fw pi-pencil',
            //             to: '/pages/crud'
            //         },
            //         {
            //             label: 'Timeline',
            //             icon: 'pi pi-fw pi-calendar',
            //             to: '/pages/timeline'
            //         },
            //         {
            //             label: 'Not Found',
            //             icon: 'pi pi-fw pi-exclamation-circle',
            //             to: '/pages/notfound'
            //         },
            //         {
            //             label: 'Empty',
            //             icon: 'pi pi-fw pi-circle-off',
            //             to: '/pages/empty'
            //         }
            //     ]
            // },
            // {
            //     label: 'Hierarchy',
            //     items: [
            //         {
            //             label: 'Submenu 1',
            //             icon: 'pi pi-fw pi-bookmark',
            //             items: [
            //                 {
            //                     label: 'Submenu 1.1',
            //                     icon: 'pi pi-fw pi-bookmark',
            //                     items: [
            //                         { label: 'Submenu 1.1.1', icon: 'pi pi-fw pi-bookmark' },
            //                         { label: 'Submenu 1.1.2', icon: 'pi pi-fw pi-bookmark' },
            //                         { label: 'Submenu 1.1.3', icon: 'pi pi-fw pi-bookmark' }
            //                     ]
            //                 },
            //                 {
            //                     label: 'Submenu 1.2',
            //                     icon: 'pi pi-fw pi-bookmark',
            //                     items: [{ label: 'Submenu 1.2.1', icon: 'pi pi-fw pi-bookmark' }]
            //                 }
            //             ]
            //         },
            //         {
            //             label: 'Submenu 2',
            //             icon: 'pi pi-fw pi-bookmark',
            //             items: [
            //                 {
            //                     label: 'Submenu 2.1',
            //                     icon: 'pi pi-fw pi-bookmark',
            //                     items: [
            //                         { label: 'Submenu 2.1.1', icon: 'pi pi-fw pi-bookmark' },
            //                         { label: 'Submenu 2.1.2', icon: 'pi pi-fw pi-bookmark' }
            //                     ]
            //                 },
            //                 {
            //                     label: 'Submenu 2.2',
            //                     icon: 'pi pi-fw pi-bookmark',
            //                     items: [{ label: 'Submenu 2.2.1', icon: 'pi pi-fw pi-bookmark' }]
            //                 }
            //             ]
            //         }
            //     ]
            // },
            // {
            //     label: 'Get Started',
            //     items: [
            //         {
            //             label: 'Documentation',
            //             icon: 'pi pi-fw pi-question',
            //             to: '/documentation'
            //         },
            //         {
            //             label: 'View Source',
            //             icon: 'pi pi-fw pi-search',
            //             url: 'https://github.com/primefaces/sakai-react',
            //             target: '_blank'
            //         }
            //     ]
            // }
        ];

        const filteredItems = model.filter((item) => {
            if (item.roles && !item.roles.includes(userRole)) {
                return false;
            }
            if (item.items) {
                item.items = item.items.filter((subItem) => !subItem.roles || subItem.roles.includes(userRole));
                return item.items.length > 0;
            }
            return true;
        });
        console.log(filteredItems);
        setFilteredModel(filteredItems);
    }, []);

    return (
        <MenuProvider>
            <ul className="layout-menu">
                {filteredModel.map((item, i) => {
                    return !item?.seperator ? <AppMenuitem item={item} root={true} index={i} key={item.label} /> : <li className="menu-separator"></li>;
                })}
            </ul>
        </MenuProvider>
    );
};

export default AppMenu;
