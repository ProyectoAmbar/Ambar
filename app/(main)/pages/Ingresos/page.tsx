'use client';

import React, { useState, useEffect } from 'react';
import { Button } from 'primereact/button';
import { BreadCrumb } from 'primereact/breadcrumb';
import { Dialog } from 'primereact/dialog';
import { MenuItem } from 'primereact/menuitem';
import { getSaldo, getHistoryTransactions, addIncomeService, addExpenseService } from '../../../api/taskService';
import Cookies from 'js-cookie';
import ExpenseModal from '../../../../demo/components/ExpenseModal';
import TransactionsTable from '../../../../demo/components/TransactionTable';
import IncomeExpenseChart from '../../../../demo/components/IncomeExpenseChart ';
import useWindowSize from '../../hooks/useWindowSize';
import './ExpensesStyles.scss';

const ExpenseView = () => {
    const [balance, setBalance] = useState(0);
    const [showAllTransactionsModal, setShowAllTransactionsModal] = useState(false);
    const [showModal, setShowModal] = useState(false);
    const [isIncome, setIsIncome] = useState(true);
    const [amount, setAmount] = useState(0);
    const [description, setDescription] = useState('');
    const [transactions, setTransactions] = useState([]);
    const { width } = useWindowSize();
    const home: MenuItem = { icon: 'pi pi-home', url: '/' };
    const breadcrumbItems: MenuItem[] = [{ label: 'Formularios' }, { label: 'Ingresos y Egresos' }];
    const openModal = (income) => {
        setIsIncome(income);
        setShowModal(true);
    };

    useEffect(() => {
        fetchTransactions();
        fetchSaldo();
    }, []);

    const fetchTransactions = async () => {
        const fetchedTransactions = await getHistoryTransactions();
        setTransactions(fetchedTransactions);
    };

    const fetchSaldo = async () => {
        const saldoData = await getSaldo();
        setBalance(saldoData.saldo);
    };

    const handleTransaction = async (transactionData, isIncome) => {
        const empleadoId = Cookies.get('idEmpleado');
        const data = {
            saldo: transactionData.saldo,
            descripcion: transactionData.descripcion,
            empleado: empleadoId
        };

        try {
            if (isIncome) {
                await addIncomeService(data);
            } else {
                await addExpenseService(data);
            }
            await fetchTransactions();
            await fetchSaldo();
        } catch (error) {
            console.error('Error al realizar la transacción:', error);
        }
    };

    return (
        <div className="containerFormTask">
            <div className="col-12 ">
                <div className="card">
                    <h5>Ver Ingresos y Egresos</h5>
                    <BreadCrumb home={home} model={breadcrumbItems} />
                </div>
            </div>
            <div className="col-12 ">
                <div className="card">
                    <div>
                        <h3>Saldo Actual: COP {balance.toLocaleString()}</h3>
                        <div className="flex items-center justify-between mb-4 containerbuttons">
                            <div className="my-4">
                                <Button label="Ingresar Dinero" icon="pi pi-plus" onClick={() => openModal(true)} className="p-button-success mr-4" />
                                <Button label="Retirar Dinero" icon="pi pi-minus" onClick={() => openModal(false)} className="p-button-danger mr-4" />
                                <Button label="Ver Todas las Transacciones" onClick={() => setShowAllTransactionsModal(true)} />
                                <Dialog visible={showAllTransactionsModal} onHide={() => setShowAllTransactionsModal(false)}>
                                    <TransactionsTable transactions={transactions} filterByToday={false} />
                                </Dialog>
                            </div>

                            <div style={{ width: '300px' }}>
                                {' '}
                                <IncomeExpenseChart transactions={transactions} />
                            </div>
                        </div>

                        <TransactionsTable transactions={transactions} filterByToday={true} />

                        <ExpenseModal showModal={showModal} setShowModal={setShowModal} isIncome={isIncome} amount={amount} setAmount={setAmount} description={description} setDescription={setDescription} handleTransaction={handleTransaction} />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ExpenseView;
