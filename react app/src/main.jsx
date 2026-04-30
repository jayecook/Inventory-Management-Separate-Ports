import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import "./style.css";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

function App() {
  const [products, setProducts] = useState([]);
  const [form, setForm] = useState({ name: "", stock: "", amount: "" });
  const [editingId, setEditingId] = useState(null);
  const [message, setMessage] = useState("");

  async function loadProducts() {
    const response = await fetch(`${API_BASE_URL}/products`);
    const data = await response.json();
    setProducts(data);
  }

  useEffect(() => {
    loadProducts().catch(() => setMessage("Could not connect to the FastAPI REST API on port 8000."));
  }, []);

  function handleChange(event) {
    setForm({ ...form, [event.target.name]: event.target.value });
  }

  function resetForm() {
    setForm({ name: "", stock: "", amount: "" });
    setEditingId(null);
  }

  async function handleSubmit(event) {
    event.preventDefault();
    const payload = {
      name: form.name,
      stock: Number(form.stock),
      amount: Number(form.amount),
    };

    const url = editingId ? `${API_BASE_URL}/products/${editingId}` : `${API_BASE_URL}/products`;
    const method = editingId ? "PUT" : "POST";

    await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    resetForm();
    loadProducts();
  }

  function startEdit(product) {
    setEditingId(product.id);
    setForm({ name: product.name, stock: product.stock, amount: product.amount });
  }

  async function deleteProduct(id) {
    await fetch(`${API_BASE_URL}/products/${id}`, { method: "DELETE" });
    loadProducts();
  }

  return (
    <main className="page">
      <section className="hero">
        <div>
          <h1>Inventory React App</h1>
          <p>React runs on port 3000. FastAPI REST API runs on port 8000.</p>
        </div>
        <a href="http://localhost:5000" target="_blank">Open Product Table</a>
      </section>

      {message && <p className="message">{message}</p>}

      <form className="card form" onSubmit={handleSubmit}>
        <input name="name" placeholder="Product name" value={form.name} onChange={handleChange} required />
        <input name="stock" type="number" placeholder="Stock" value={form.stock} onChange={handleChange} required />
        <input name="amount" type="number" placeholder="Amount" value={form.amount} onChange={handleChange} required />
        <button type="submit">{editingId ? "Update" : "Add"} Product</button>
        {editingId && <button type="button" onClick={resetForm}>Cancel</button>}
      </form>

      <section className="card">
        <table>
          <thead>
            <tr><th>ID</th><th>Name</th><th>Stock</th><th>Amount</th><th>Status</th><th>Actions</th></tr>
          </thead>
          <tbody>
            {products.map((product) => (
              <tr key={product.id}>
                <td>{product.id}</td>
                <td>{product.name}</td>
                <td>{product.stock}</td>
                <td>{product.amount}</td>
                <td><span className={product.status === "LOW STOCK" ? "low" : "ok"}>{product.status}</span></td>
                <td>
                  <button onClick={() => startEdit(product)}>Edit</button>
                  <button className="danger" onClick={() => deleteProduct(product.id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);
