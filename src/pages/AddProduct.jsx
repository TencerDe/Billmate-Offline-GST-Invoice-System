import React, { useState } from 'react';

const AddProduct = () => {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    hsn_code: '',
    price: '',
    gst_rate: ''
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

    const response = await fetch('http://127.0.0.1:12/api/add-product/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        ...formData,
        price: parseFloat(formData.price),
        gst_rate: parseFloat(formData.gst_rate)
      })
    });

    const data = await response.json();
    if (response.ok) {
      setMessage('Product added successfully!');
      setFormData({ name: '', description: '', hsn_code: '', price: '', gst_rate: '' });
    } else {
      setMessage('Error: ' + (data.message || 'Unable to add product.'));
    }
  };

  return (
    <div>
      <h2>Add Product</h2>
      <form onSubmit={handleSubmit}>
        <input name="name" placeholder="Name" value={formData.name} onChange={handleChange} required />
        <input name="description" placeholder="Description" value={formData.description} onChange={handleChange} />
        <input name="hsn_code" placeholder="HSN Code" value={formData.hsn_code} onChange={handleChange} required />
        <input name="price" type="number" placeholder="Price" value={formData.price} onChange={handleChange} required />
        <input name="gst_rate" type="number" placeholder="GST Rate (%)" value={formData.gst_rate} onChange={handleChange} required />
        <button type="submit">Add Product</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default AddProduct;
