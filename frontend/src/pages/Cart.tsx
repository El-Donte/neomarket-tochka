import { useCart } from '../store/CartContext';
import { Trash2, Plus, Minus, CreditCard } from 'lucide-react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import apiClient from '../api/client';
import { toast } from 'react-hot-toast';

const Cart = () => {
  const { items, removeFromCart, updateQuantity, clearCart, totalItems } = useCart();
  const navigate = useNavigate();

  const totalPrice = items.reduce((sum, item) => sum + item.sku.price * item.quantity, 0);

  const handleCheckout = async () => {
    try {
      
      const invoiceData = {
        number: `INV-${Date.now()}`,
        comment: "Order from web cart",
        items: items.map(item => ({
          sku_id: item.sku.id,
          quantity: item.quantity,
          purchase_price: item.sku.price 
        }))
      };

      await apiClient.post('/invoices', invoiceData);
      clearCart();
      toast.success('Накладная успешно создана!');
      navigate('/dashboard'); 
    } catch (err) {
      console.error('Checkout failed:', err);
      toast.error('Ошибка при создании накладной.');
    }
  };

  return (
    <div style={{ paddingTop: '100px', paddingBottom: '50px' }}>
      <div className="container">
        <header style={{ marginBottom: '2rem' }}>
          <h1 style={{ fontSize: '2.5rem', marginBottom: '0.5rem', fontWeight: '800' }}>
            <span className="gradient-text">Новая поставка</span>
          </h1>
          <p style={{ color: 'var(--text-muted)' }}>{totalItems} позиций в черновике</p>
        </header>

        {items.length === 0 ? (
          <div className="glass" style={{ padding: '4rem', textAlign: 'center', borderRadius: 'var(--radius-lg)' }}>
            <p style={{ fontSize: '1.2rem', color: 'var(--text-muted)', marginBottom: '2rem' }}>Ваша корзина пуста.</p>
            <button onClick={() => navigate('/catalog')} className="btn-primary">В каталог</button>
          </div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 300px', gap: '2rem', alignItems: 'start' }}>
            {}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {items.map(item => (
                <motion.div 
                  layout
                  key={item.sku.id} 
                  className="glass" 
                  style={{ padding: '1.5rem', borderRadius: 'var(--radius-md)', display: 'flex', gap: '1.5rem', alignItems: 'center' }}
                >
                  <div style={{ width: '80px', height: '80px', background: 'rgba(255,255,255,0.05)', borderRadius: '12px' }}></div>
                  <div style={{ flex: 1 }}>
                    <h3 style={{ fontSize: '1.1rem', marginBottom: '0.25rem' }}>{item.sku.name}</h3>
                    <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>SKU: {item.sku.id}</p>
                  </div>
                  
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', background: 'rgba(255,255,255,0.08)', padding: '0.5rem', borderRadius: '10px' }}>
                    <button onClick={() => updateQuantity(item.sku.id, item.quantity - 1)} style={{ color: 'white' }}><Minus size={16} /></button>
                    <span style={{ width: '20px', textAlign: 'center', fontWeight: 'bold', color: 'white' }}>{item.quantity}</span>
                    <button onClick={() => updateQuantity(item.sku.id, item.quantity + 1)} style={{ color: 'white' }}><Plus size={16} /></button>
                  </div>
                  
                  <div style={{ width: '80px', textAlign: 'right', fontWeight: 'bold' }}>
                    ${item.sku.price * item.quantity}
                  </div>
                  
                  <button onClick={() => removeFromCart(item.sku.id)} style={{ color: '#f87171' }}>
                    <Trash2 size={18} />
                  </button>
                </motion.div>
              ))}
            </div>

            {}
            <div className="glass" style={{ padding: '2rem', borderRadius: 'var(--radius-lg)', position: 'sticky', top: '100px' }}>
              <h2 style={{ fontSize: '1.2rem', marginBottom: '1.5rem', fontWeight: '800' }}>Итого</h2>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem' }}>
                <span style={{ color: 'var(--text-muted)' }}>Сумма</span>
                <span>${totalPrice}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1.5rem', paddingBottom: '1.5rem', borderBottom: '1px solid var(--border-color)' }}>
                <span style={{ color: 'var(--text-muted)' }}>Налог (0%)</span>
                <span>$0</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '2rem', fontSize: '1.2rem', fontWeight: 'bold' }}>
                <span>Всего</span>
                <span className="gradient-text">${totalPrice}</span>
              </div>
              
              <button 
                onClick={handleCheckout}
                className="btn-primary" 
                style={{ width: '100%', padding: '1rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}
              >
                <CreditCard size={18} /> Создать накладную
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Cart;

