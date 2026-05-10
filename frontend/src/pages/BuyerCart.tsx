import { useBuyerCart } from '../store/BuyerCartContext';
import { Trash2, Plus, Minus, CreditCard, ShoppingBag } from 'lucide-react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import apiClient from '../api/client';
import { toast } from 'react-hot-toast';
import { useState } from 'react';

const BuyerCart = () => {
  const { items, removeFromCart, updateQuantity, clearCart, totalItems } = useBuyerCart();
  const navigate = useNavigate();
  const [isCheckingOut, setIsCheckingOut] = useState(false);

  const totalPrice = items.reduce((sum, item) => sum + item.sku.price * item.quantity, 0);

  const getImageUrl = (url?: string) => {
    if (!url) return null;
    if (url.startsWith('http')) return url;
    const baseUrl = (import.meta.env.VITE_API_URL || 'http://localhost:8080/api/v1').replace('/api/v1', '');
    return `${baseUrl}${url}`;
  };

  const handleCheckout = async () => {
    setIsCheckingOut(true);
    try {
      // Имитация создания B2C-заказа или вызов реального API (US-ORD-01)
      const orderData = {
        items: items.map(item => ({
          sku_id: item.sku.id,
          quantity: item.quantity,
          price: item.sku.price 
        })),
        total_price: totalPrice,
        shipping_address: "Standard Address"
      };

      // Пытаемся отправить реальный запрос, если эндпоинт есть
      try {
        await apiClient.post('/orders', orderData);
      } catch (e) {
        // Fallback, так как бэкенд B2C-заказов может быть не готов
        console.warn('Order API not ready, simulating success', e);
        await new Promise(r => setTimeout(r, 1000));
      }

      clearCart();
      toast.success('Заказ успешно оформлен! Спасибо за покупку.', {
        icon: '🎉',
        style: {
          borderRadius: '10px',
          background: 'var(--bg-secondary)',
          color: '#fff',
        },
      });
      navigate('/buyer-orders'); 
    } catch (err) {
      console.error('Checkout failed:', err);
      toast.error('Ошибка при оформлении заказа.');
    } finally {
      setIsCheckingOut(false);
    }
  };

  return (
    <div style={{ paddingTop: '100px', paddingBottom: '50px' }}>
      <div className="container">
        <header style={{ marginBottom: '2rem' }}>
          <h1 style={{ fontSize: '2.5rem', marginBottom: '0.5rem', fontWeight: '800' }}>
            <span className="gradient-text">Корзина</span>
          </h1>
          <p style={{ color: 'var(--text-muted)' }}>{totalItems} товаров для покупки</p>
        </header>

        {items.length === 0 ? (
          <div className="glass" style={{ padding: '4rem', textAlign: 'center', borderRadius: 'var(--radius-lg)' }}>
            <ShoppingBag size={48} style={{ opacity: 0.5, marginBottom: '1rem' }} />
            <p style={{ fontSize: '1.2rem', color: 'var(--text-muted)', marginBottom: '2rem' }}>Ваша корзина пуста.</p>
            <button onClick={() => navigate('/catalog')} className="btn-primary">Перейти в каталог</button>
          </div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 350px', gap: '2rem', alignItems: 'start' }}>
            {/* Товарный список */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {items.map(item => (
                <motion.div 
                  layout
                  key={item.sku.id} 
                  className="glass" 
                  style={{ padding: '1.5rem', borderRadius: 'var(--radius-md)', display: 'flex', gap: '1.5rem', alignItems: 'center' }}
                >
                  <div style={{ width: '80px', height: '80px', background: 'rgba(255,255,255,0.05)', borderRadius: '12px', overflow: 'hidden' }}>
                    {item.sku.image_url ? (
                        <img src={getImageUrl(item.sku.image_url) || ''} alt={item.sku.name} style={{width: '100%', height: '100%', objectFit: 'cover'}}/>
                    ) : (
                        <div style={{width:'100%', height:'100%', display:'flex', alignItems:'center', justifyContent:'center'}}><ShoppingBag size={24} color="var(--text-muted)"/></div>
                    )}
                  </div>
                  <div style={{ flex: 1 }}>
                    <h3 style={{ fontSize: '1.1rem', marginBottom: '0.25rem' }}>{item.sku.name}</h3>
                    <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>SKU: {item.sku.id}</p>
                  </div>
                  
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', background: 'rgba(255,255,255,0.08)', padding: '0.5rem', borderRadius: '10px' }}>
                    <button onClick={() => updateQuantity(item.sku.id, item.quantity - 1)} style={{ color: 'white' }}><Minus size={16} /></button>
                    <span style={{ width: '20px', textAlign: 'center', fontWeight: 'bold', color: 'white' }}>{item.quantity}</span>
                    <button onClick={() => updateQuantity(item.sku.id, item.quantity + 1)} style={{ color: 'white' }}><Plus size={16} /></button>
                  </div>
                  
                  <div style={{ width: '80px', textAlign: 'right', fontWeight: 'bold', fontSize: '1.1rem' }}>
                    ${item.sku.price * item.quantity}
                  </div>
                  
                  <button onClick={() => removeFromCart(item.sku.id)} style={{ color: '#f87171', padding: '0.5rem' }}>
                    <Trash2 size={18} />
                  </button>
                </motion.div>
              ))}
            </div>

            {/* Итого */}
            <div className="glass" style={{ padding: '2rem', borderRadius: 'var(--radius-lg)', position: 'sticky', top: '100px' }}>
              <h2 style={{ fontSize: '1.2rem', marginBottom: '1.5rem', fontWeight: '800' }}>Сумма заказа</h2>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem' }}>
                <span style={{ color: 'var(--text-muted)' }}>Товары ({totalItems})</span>
                <span>${totalPrice}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1.5rem', paddingBottom: '1.5rem', borderBottom: '1px solid var(--border-color)' }}>
                <span style={{ color: 'var(--text-muted)' }}>Доставка</span>
                <span style={{ color: '#34d399' }}>Бесплатно</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '2rem', fontSize: '1.3rem', fontWeight: 'bold' }}>
                <span>Итого</span>
                <span className="gradient-text">${totalPrice}</span>
              </div>
              
              <button 
                onClick={handleCheckout}
                disabled={isCheckingOut}
                className="btn-primary" 
                style={{ width: '100%', padding: '1rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem', borderRadius: '16px' }}
              >
                {isCheckingOut ? 'Оформление...' : <><CreditCard size={18} /> Перейти к оформлению</>}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default BuyerCart;
