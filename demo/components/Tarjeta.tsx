import React from 'react';
import { FaCalendarAlt, FaTag, FaUser } from 'react-icons/fa';
import '../../styles/Pages/Tarjeta.css'
interface TarjetaProps {
    tipo: 'ingreso' | 'egreso';
    fecha: string;
    valor: number;
    descripcion: string;
    persona: string;
}

const Tarjeta: React.FC<TarjetaProps> = ({ tipo, fecha, valor, descripcion, persona }) => {
    return (
        <div className={`p-5  ingresosTarjeta ${tipo==='ingreso' ? 'bg-green' :'bg-red'}  `}>
            <div className="justify-between p-1 sm:flex">
                <div className="flex-1">
                    <h3 className={`text-2xl font-medium `}>
                        {tipo.charAt(0).toUpperCase() + tipo.slice(1)}
                    </h3>
                    <p className="descripcion mt-2 pr-2">
                        <strong>Descripción:</strong> {descripcion}
                    </p>
                </div>
                <div className="  mt-5 space-y-4 text-sm sm:mt-0 sm:space-y-2">
                    <span className="flex items-center text-gray-600">
                        <FaCalendarAlt className="mr-2 icon" />
                        <strong>Fecha:</strong><span className='text-gray-600'>{fecha}</span>
                    </span>
                    <span className="flex items-center text-gray-600">
                        <FaTag className="mr-2 icon" />
                        <strong>Valor:</strong><span className='text-gray-600'>${valor.toFixed(2)}</span>
                    </span>
                    <span className="flex items-center text-gray-600">
                        <FaUser className="mr-2 icon" />
                        <strong>Persona:</strong> <span className='text-gray-600'>{persona}</span>
                    </span>
                    {/* Aquí puedes agregar más campos con sus respectivos iconos si es necesario */}
                </div>
            </div>
        </div>
    );
}

export default Tarjeta;
