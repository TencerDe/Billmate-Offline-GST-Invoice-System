import React, { useState } from 'react';

const AddCustomer = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    address: '',
    gstin: ''
  });

  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const response = await fetch('http://127.0.0.1:12/api/add-customer/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(formData)
    });

    const data = await response.json();
    if (response.ok) {
      setMessage('Customer added successfully!');
      setFormData({ name: '', email: '', phone: '', address: '', gstin: '' });
    } else {
      setMessage('Error: ' + (data.message || 'Unable to add customer.'));
    }
  };

  return (
    <div>
      <h2>Add Customer</h2>
      <form onSubmit={handleSubmit}>
        <input name="name" placeholder="Name" value={formData.name} onChange={handleChange} required />
        <input name="email" placeholder="Email" value={formData.email} onChange={handleChange} />
        <input name="phone" placeholder="Phone" value={formData.phone} onChange={handleChange} required />
        <input name="address" placeholder="Address" value={formData.address} onChange={handleChange} required />
        <input name="gstin" placeholder="GSTIN" value={formData.gstin} onChange={handleChange} />
        <button type="submit">Add Customer</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default AddCustomer;
