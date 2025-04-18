import { Link } from 'react-router-dom'

export default function Navbar() {
  return (
    <nav style={{ padding: '1rem', backgroundColor: '#222', color: '#fff' }}>
      <Link to="/" style={{ margin: '0 10px', color: 'white' }}>Home</Link>
      <Link to="/invoices" style={{ margin: '0 10px', color: 'white' }}>Invoices</Link>
      <Link to="/add-customer" style={{ margin: '0 10px', color: 'white' }}>Add Customer</Link>
      <Link to="/add-product" style={{ margin: '0 10px', color: 'white' }}>Add Product</Link>
      <Link to="/create-invoice" style={{ margin: '0 10px', color: 'white' }}>Create Invoice</Link>
    </nav>
  )
}
