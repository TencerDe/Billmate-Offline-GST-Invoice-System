import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div>
      <h1>Welcome to BillMate</h1>
      <p>This is your GST-ready invoice billing system.</p>

      <div style={{ marginTop: '20px' }}>
        <Link to="/add-customer">Add Customer</Link> |{' '}
        <Link to="/add-product">Add Product</Link> |{' '}
        <Link to="/create-invoice">Create Invoice</Link> |{' '}
        <Link to="/invoices">View Invoices</Link>
      </div>
    </div>
  );
};

export default Home;
