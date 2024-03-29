'use client';
import React, { useEffect, useState } from 'react';
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import esLocale from '@fullcalendar/core/locales/es';
import Swal from 'sweetalert2';
import withReactContent from 'sweetalert2-react-content';
import { AllTaskPending, TaskCitaPrimera, MakeupTask,PhotoTask } from '../../../api/taskService';

interface Event {
    id: string;
    title: string;
    date: string;
    color: string;
    allDay: boolean;
    eventType: string;
}

interface Task {
    _id: string;
    fechaEntrega: string;
    entregaCompletado: boolean;
}

const MyFullCalendar = () => {
    const [events, setEvents] = useState<Event[]>([]);
    const [selectedDate, setSelectedDate] = useState<string | null>(null);

    const MySwal = withReactContent(Swal);

    useEffect(() => {
        const fetchEvents = async () => {
            try {
                const [apitask, apiCitaPrimera, apiMakeup,apiPhotos] = await Promise.all([AllTaskPending(), TaskCitaPrimera(), MakeupTask(),PhotoTask()]);

                const mappedTasks = apitask.map((task) => ({
                    id: task._id,
                    title: 'Fecha de entrega del alquiler',
                    date: task.fechaEntrega,
                    color: task.entregaCompletado ? 'green' : 'red',
                    allDay: true,
                    eventType: 'task',
                    state:task.entregaCompletado

                }));

                const mappedCitas = apiCitaPrimera.map((cita) => {
                    const date = new Date(cita.fecha);
                    const formattedDate = date.toISOString().split('T')[0];
                    return {
                        id: cita._id,
                        title: 'Cita de Primera Vez - ' + cita.motivo,
                        date: formattedDate,
                        color: cita.estado ? 'blue' : 'orange',
                        allDay: true,
                        eventType: 'citaPrimera',
                        state:cita.estado
                    };
                });

                const mappedMakeup = apiMakeup.map((makeup) => {
                    const date = new Date(makeup.fecha);
                    const formattedDate = date.toISOString().split('T')[0];
                    return {
                        id: makeup._id,
                        title: `Makeup para ${makeup.tipoMakeup}`,
                        date: formattedDate,
                        color: makeup.completado ? 'purple' : 'pink',
                        allDay: true,
                        eventType: 'makeup',
                        state:makeup.completado

                    };
                });

                const mappedPhotos = apiPhotos.map((photo) => {
                    const date = new Date(photo.fecha);
                    const formattedDate = date.toISOString().split('T')[0];
                    return {
                        id: photo._id,
                        title: `Sesion de fotos para ${photo.nombreCliente}`,
                        date: formattedDate,
                        color: photo.estado ? 'brown' : 'pink',
                        allDay: true,
                        eventType: 'photo',
                        state:photo.estado

                    };
                });

                setEvents([...mappedTasks, ...mappedCitas, ...mappedMakeup,...mappedPhotos]);
            } catch (error) {
                console.error('Error al obtener los eventos', error);
            }
        };

        fetchEvents();
    }, []);

    const handleEventClick = (clickInfo) => {
        clickInfo.jsEvent.preventDefault();
        const { event } = clickInfo;
        let modalContent;
        if (event.extendedProps.eventType === 'task') {
            const estado = event.extendedProps.state ? 'Completado' : 'Sin completar';
            modalContent = (
                <div>
                    <p>ID del evento: {event.id}</p>
                    <p>Fecha de entrega: {event.startStr}</p>
                    <p>Estado: {estado}</p>
                </div>
            );
        } else if (event.extendedProps.eventType === 'citaPrimera') {
            const estado = event.extendedProps.state ? 'Completado' : 'Sin completar';
            console.log(event);
            modalContent = (
            
                <div>
                    <p>ID de la cita: {event.id}</p>
                    <p>Fecha de la cita: {event.startStr}</p>
                    <p>Estado: {estado}</p>
                </div>
            );
        } else if (event.extendedProps.eventType === 'makeup') {
            const estado = event.extendedProps.state ? 'Completado' : 'Sin completar';
            modalContent = (
                <div>
                    <p>ID del evento de maquillaje: {event.id}</p>
                    <p>Tipo de maquillaje: {event.title}</p>
                    <p>Fecha: {event.startStr}</p>
                    <p>Estado: {estado}</p>
                </div>
            );
        }else if (event.extendedProps.eventType === 'photo') {
            const estado = event.extendedProps.state ? 'Completado' : 'Sin completar';
            modalContent = (
                <div>
                    <p>ID de la sesion de fotos: {event.id}</p>
                    <p>Sesion de fotos para: {event.title}</p>
                    <p>Fecha: {event.startStr}</p>
                    <p>Estado: {estado}</p>
                </div>
            );
        }

        MySwal.fire({
            title: event.title,
            html: modalContent,
            icon: 'info'
        });
    };

    return (
        <div>
            <FullCalendar
                plugins={[dayGridPlugin]}
                initialView="dayGridMonth"
                events={events}
                locale={esLocale}
                eventClick={handleEventClick}
                eventContent={(contentInfo) => {
                    const { event } = contentInfo;
                    return {
                        html: `<div style="font-size: 14px; padding: 4px;">
                                <span class="fc-event-dot" style="background-color: ${event.backgroundColor}"></span>
                                ${event.title}
                            </div>`
                    };
                }}
                dayMaxEvents={true}
            />
            {selectedDate && (
                <div className="expanded-events-list">
                    {events
                        .filter((event) => event.date === selectedDate)
                        .map((event) => (
                            <div key={event.id} className="event">
                                <p>{event.title}</p>
                                <p>Fecha: {event.date}</p>
                            </div>
                        ))}
                </div>
            )}
        </div>
    );
};

export default MyFullCalendar;
