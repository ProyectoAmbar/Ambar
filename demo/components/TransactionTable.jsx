import React, { useState } from 'react';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { format, parseISO, startOfDay, isSameDay } from 'date-fns';
import { InputText } from 'primereact/inputtext';
import { Calendar } from 'primereact/calendar'

const TransactionsTable = ({ transactions, filterByToday }) => {
    const [globalFilter, setGlobalFilter] = useState('');
    const [selectedDate, setSelectedDate] = useState(null);

    const initialFilteredTransactions = filterByToday
        ? transactions.filter(t => {
            const transactionDate = parseISO(t.fecha_Hora);
            return isSameDay(transactionDate, startOfDay(new Date()));
          })
        : transactions;

    const filteredTransactions = selectedDate
        ? initialFilteredTransactions.filter(t => {
            const transactionDate = parseISO(t.fecha_Hora);
            return isSameDay(transactionDate, startOfDay(selectedDate));
          })
        : initialFilteredTransactions;

    const amountTemplate = (rowData) => (
        <span className={rowData.cantidad >= 0 ? 'text-success' : 'text-danger'}>
            ${rowData.cantidad.toLocaleString()}
        </span>
    );

    const dateTemplate = (rowData) => format(parseISO(rowData.fecha_Hora), 'PPPp');

    const header = (
        <div className="table-header">
            <span className="p-input-icon-left">
                <i className="pi pi-search" />
                <InputText type="search" onInput={(e) => setGlobalFilter(e.target.value)} placeholder="Buscar..." />
            </span>
            {!filterByToday && (
                <Calendar value={selectedDate} onChange={(e) => setSelectedDate(e.value)} dateFormat="dd/mm/yy" placeholder="Filtrar por fecha" showIcon />
            )}
        </div>
    );

    return (
        <DataTable value={filteredTransactions} paginator rows={10} globalFilter={globalFilter} header={header}>
            <Column field="_id" header="ID" sortable></Column>
            <Column field="cantidad" header="Cantidad" body={amountTemplate} sortable></Column>
            <Column field="descripcion" header="Descripción" sortable></Column>
            <Column field="fecha_Hora" header="Fecha y Hora" body={dateTemplate} sortable></Column>
            <Column field="metodo" header="Método" sortable></Column>
        </DataTable>
    );
};

export default TransactionsTable;
