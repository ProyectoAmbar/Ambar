import React, { useMemo } from 'react';
import { Chart } from 'primereact/chart';
import { parseISO, startOfDay, isSameDay } from 'date-fns';

const IncomeExpenseChart = ({ transactions }) => {
    const chartData = useMemo(() => {
        const todayTransactions = transactions.filter(t => isSameDay(parseISO(t.fecha_Hora), startOfDay(new Date())));

        const income = todayTransactions.filter(t => t.metodo === "Deposito").reduce((acc, t) => acc + t.cantidad, 0);
        const expenses = todayTransactions.filter(t => t.metodo.includes("retiro")).reduce((acc, t) => acc + Math.abs(t.cantidad), 0);

        return {
            labels: ['Ingresos', 'Egresos'],
            datasets: [{
                data: [income, expenses],
                backgroundColor: [
                    '#42A5F5', 
                    '#FF6384'  
                ],
                hoverBackgroundColor: [
                    '#64B5F6',
                    '#FF6384'
                ]
            }]
        };
    }, [transactions]);

    return <Chart type="pie" data={chartData} style={{ width: '100%', height: 'auto' }} />;
};
export default IncomeExpenseChart;
