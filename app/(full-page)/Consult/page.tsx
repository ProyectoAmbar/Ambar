'use client';
import React, { useState } from 'react';
import OrderTrackingInput from '../../../demo/components/OrderTrackingInput';
import OrderTrackingResults from '../../../demo/components/OrderTrackingResults';
import { OrderInfo } from '../../../types/demo';


const OrderTracking: React.FC = () => {
  const [currentOrder, setCurrentOrder] = useState<OrderInfo | null>(null);

  const handleSearch = (code: string) => {
    //espacio consulta 
    const exampleOrder: OrderInfo = {
      code: '12345',
      status: 'cita',
      descripcion:"Ejemplo de la consulta no se"
    };

    if (code === '12345') {
      setCurrentOrder(exampleOrder);
    } else {
      setCurrentOrder(null);
    }
  }

  return (
    <div>
      <OrderTrackingInput onSearch={handleSearch} />
      <OrderTrackingResults orderInfo={currentOrder} />
    </div>
  );
}

export default OrderTracking;
