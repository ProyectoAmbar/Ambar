import React from 'react';
import { Dialog } from 'primereact/dialog';
import { Button } from 'primereact/button';
import { InputNumber } from 'primereact/inputnumber';
import { InputTextarea } from 'primereact/inputtextarea';
import Cookies from 'js-cookie';

const ExpenseModal = ({ showModal, setShowModal, isIncome, amount, setAmount, description, setDescription, handleTransaction }) => {
    const headerTitle = isIncome ? "Ingreso de Dinero" : "Egreso de Dinero";

    const save = () => {
        const empleadoId = Cookies.get('idEmpleado'); 
        const transactionData = {
            saldo: amount,
            descripcion: description,
            empleado: empleadoId
        };
        handleTransaction(transactionData, isIncome);
        setShowModal(false);
    };

    const transactionDialogFooter = (
        <React.Fragment>
            <Button label="Cancelar" icon="pi pi-times" className="p-button-text" onClick={() => setShowModal(false)} />
            <Button label="Guardar" icon="pi pi-check" className="p-button-text" onClick={save} />
        </React.Fragment>
    );

    return (
        <Dialog visible={showModal} style={{ width: '450px' }} header={headerTitle} modal className="p-fluid" footer={transactionDialogFooter} onHide={() => setShowModal(false)}>
            <div className="field">
                <label htmlFor="amount">Cantidad</label>
                <InputNumber id="amount" value={amount} onValueChange={(e) => setAmount(e.value)} mode="currency" currency="COP" locale="es-CO" />
            </div>
            <div className="field">
                <label htmlFor="description">Descripción</label>
                <InputTextarea id="description" value={description} onChange={(e) => setDescription(e.target.value)} required rows={3} cols={20} />
            </div>
        </Dialog>
    );
};

export default ExpenseModal;
