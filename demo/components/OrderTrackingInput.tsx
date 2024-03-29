import React, { useState } from 'react';

const OrderTrackingInput: React.FC<{ onSearch: (code: string) => void }> = ({ onSearch }) => {
    const [code, setCode] = useState('');

    return (
        <div>
            <input
                type="text"
                value={code}
                onChange={e => setCode(e.target.value)}
                placeholder="Ingresa el código de factura"
            />
            <button onClick={() => onSearch(code)}>Buscar</button>
        </div>
    );
}

export default OrderTrackingInput;
