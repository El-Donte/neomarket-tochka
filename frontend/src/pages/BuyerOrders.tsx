import { ShoppingBag, XCircle } from 'lucide-react';
import { toast } from 'react-hot-toast';

// Мок-данные для заказов, так как бэкенд B2C-заказов может быть не готов
const MOCK_ORDERS = [
  {
    id: "ORD-12345",
    status: "PROCESSING",
    date: "2026-05-10T10:00:00Z",
    total: 499,
    items: [
      { name: "Quantum Watch Series 7", quantity: 1, price: 499 }
    ]
  }
];

const BuyerOrders = () => {

  const handleCancelOrder = (id: string) => {
    toast.success(`Заказ ${id} успешно отменен.`);
    // В реальности здесь будет вызов API отмены заказа (US-ORD-03)
  };

  return (
    <div style={{ paddingTop: '100px', paddingBottom: '50px' }}>
      <div className="container">
        <header style={{ marginBottom: '3rem' }}>
          <h1 style={{ fontSize: '2.5rem', marginBottom: '0.5rem', fontWeight: '800' }}>
            <span className="gradient-text">Мои заказы</span>
          </h1>
          <p style={{ color: 'var(--text-muted)' }}>История ваших покупок и управление заказами.</p>
        </header>

        <div className="glass" style={{ borderRadius: 'var(--radius-lg)', overflow: 'hidden' }}>
            {MOCK_ORDERS.length === 0 ? (
              <div style={{ padding: '4rem', textAlign: 'center', color: 'var(--text-muted)' }}>
                <ShoppingBag size={48} style={{ marginBottom: '1rem', opacity: 0.5 }} />
                <p>Вы еще ничего не заказали.</p>
              </div>
            ) : (
              <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead style={{ background: 'rgba(255,255,255,0.03)', borderBottom: '1px solid var(--border-color)' }}>
                  <tr>
                    <th style={{ padding: '1.2rem 1.5rem', textAlign: 'left', color: 'var(--text-muted)' }}>НОМЕР ЗАКАЗА</th>
                    <th style={{ padding: '1.2rem 1.5rem', textAlign: 'left', color: 'var(--text-muted)' }}>ДАТА</th>
                    <th style={{ padding: '1.2rem 1.5rem', textAlign: 'left', color: 'var(--text-muted)' }}>ТОВАРЫ</th>
                    <th style={{ padding: '1.2rem 1.5rem', textAlign: 'left', color: 'var(--text-muted)' }}>СУММА</th>
                    <th style={{ padding: '1.2rem 1.5rem', textAlign: 'left', color: 'var(--text-muted)' }}>СТАТУС</th>
                    <th style={{ padding: '1.2rem 1.5rem', textAlign: 'right', color: 'var(--text-muted)' }}>ДЕЙСТВИЯ</th>
                  </tr>
                </thead>
                <tbody>
                  {MOCK_ORDERS.map(order => (
                    <tr key={order.id} style={{ borderBottom: '1px solid var(--border-color)' }}>
                      <td style={{ padding: '1.2rem 1.5rem', fontWeight: 'bold' }}>{order.id}</td>
                      <td style={{ padding: '1.2rem 1.5rem', color: 'var(--text-muted)' }}>
                        {new Date(order.date).toLocaleDateString()}
                      </td>
                      <td style={{ padding: '1.2rem 1.5rem' }}>
                        {order.items.map((i, idx) => (
                           <div key={idx} style={{ fontSize: '0.9rem' }}>{i.name} (x{i.quantity})</div>
                        ))}
                      </td>
                      <td style={{ padding: '1.2rem 1.5rem', fontWeight: 'bold' }}>${order.total}</td>
                      <td style={{ padding: '1.2rem 1.5rem' }}>
                        <span style={{ 
                            background: 'rgba(99, 102, 241, 0.1)', 
                            color: 'var(--accent-primary)', 
                            padding: '0.3rem 0.8rem', 
                            borderRadius: '12px', 
                            fontSize: '0.8rem', 
                            fontWeight: 'bold' 
                        }}>
                          В ОБРАБОТКЕ
                        </span>
                      </td>
                      <td style={{ padding: '1.2rem 1.5rem', textAlign: 'right' }}>
                        <button 
                            onClick={() => handleCancelOrder(order.id)}
                            className="glass-btn" 
                            style={{ color: '#f87171', display: 'inline-flex', alignItems: 'center', gap: '0.4rem', padding: '0.5rem 1rem' }}
                        >
                          <XCircle size={16} /> Отменить
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
        </div>
      </div>
    </div>
  );
};

export default BuyerOrders;
