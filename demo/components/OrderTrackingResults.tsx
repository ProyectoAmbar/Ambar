import React from 'react';
import { OrderInfo } from '../../types/demo'; 

const OrderTrackingResults: React.FC<{ orderInfo: OrderInfo | null }> = ({ orderInfo }) => {
    if (!orderInfo) {
        return <div>Upps, no encontramos tu factura.</div>;
    }

    return (
        <div>
            <div>
                {/* Aquí puedes implementar la línea de tiempo visual usando el estado orderInfo.status */}
            </div>
            <div>
                
                Código: {orderInfo.code}
            <h3>{orderInfo.descripcion}</h3>
            </div>
        </div>
    );
}

export default OrderTrackingResults;
