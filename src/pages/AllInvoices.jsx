import React, { useEffect, useState } from 'react';

const AllInvoices = () => {
  const [invoices, setInvoices] = useState([]);

  useEffect(() => {
    const fetchInvoices = async () => {
      try {
        const res = await fetch('http://127.0.0.1:12/api/invoices/');
        const data = await res.json();
        setInvoices(data.invoices || []);
      } catch (error) {
        console.error('Error fetching invoices:', error);
      }
    };

    fetchInvoices();
  }, []);

  return (
    <div>
      <h2>All Invoices</h2>
      {invoices.length === 0 ? (
        <p>No invoices found.</p>
      ) : (
        <table border="1" cellPadding="10">
          <thead>
            <tr>
              <th>ID</th>
              <th>Invoice Number</th>
              <th>Customer</th>
              <th>Total Amount</th>
              <th>Total Tax</th>
              <th>Created At</th>
              <th>PDF</th>
            </tr>
          </thead>
          <tbody>
            {invoices.map((invoice) => (
              <tr key={invoice.id}>
                <td>{invoice.id}</td>
                <td>{invoice.invoice_number}</td>
                <td>{invoice.customer_name}</td>
                <td>₹{invoice.total_amount.toFixed(2)}</td>
                <td>₹{invoice.total_tax.toFixed(2)}</td>
                <td>{new Date(invoice.created_at).toLocaleString()}</td>
                <td>
                  <a href={`http://127.0.0.1:12/api/invoices/${invoice.id}/pdf/`} target="_blank" rel="noopener noreferrer">
                    Download
                  </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default AllInvoices;
