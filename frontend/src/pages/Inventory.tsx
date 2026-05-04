import { useState, useEffect } from 'react';
import apiClient from '../api/client';
import { Package, AlertTriangle, Search, RefreshCw, PlusCircle } from 'lucide-react';
import { useCart } from '../store/CartContext';
import { toast } from 'react-hot-toast';

interface InventoryItem {
  sku_id: number;
  sku_name: string;
  product_title: string;
  price: number;
  quantity: number;
  updated_at: string;
}

const Inventory = () => {
  const [inventory, setInventory] = useState<InventoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const { addToCart } = useCart();

  useEffect(() => {
    fetchInventory();
  }, []);

  const fetchInventory = async () => {
    setLoading(true);
    try {
      const response = await apiClient.get('/skus/inventory/all');
      setInventory(response.data);
    } catch (err) {
      console.error('Failed to fetch inventory:', err);
    } finally {
      setLoading(false);
    }
  };

  const filteredItems = inventory.filter(item => 
    item.product_title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    item.sku_name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div style={{ paddingTop: '100px', paddingBottom: '50px' }}>
      <div className="container">
        <header style={{ marginBottom: '3rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h1 style={{ fontSize: '2.5rem', marginBottom: '0.5rem', fontWeight: '800' }}>
              <span className="gradient-text">Инвентарь</span>
            </h1>
            <p style={{ color: 'var(--text-muted)' }}>Текущие остатки товаров и управление запасами.</p>
          </div>
          
          <button onClick={fetchInventory} className="glass-btn" style={{ padding: '0.8rem', borderRadius: '12px', color: 'var(--accent-secondary)' }}>
            <RefreshCw size={20} className={loading ? 'spin' : ''} />
          </button>
        </header>

        {}
        <div className="glass" style={{ padding: '1.5rem', borderRadius: 'var(--radius-lg)', marginBottom: '2rem', display: 'flex', gap: '1rem' }}>
          <div style={{ flex: 1, position: 'relative' }}>
            <Search style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} size={18} />
            <input 
              type="text" 
              placeholder="Поиск по названию или SKU..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={{ width: '100%', padding: '0.8rem 1rem 0.8rem 3rem', background: 'rgba(255,255,255,0.05)', border: '1px solid var(--border-color)', borderRadius: '12px', color: 'white' }}
            />
          </div>
        </div>

        {}
        <div className="glass" style={{ borderRadius: 'var(--radius-lg)', overflow: 'hidden' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
            <thead style={{ background: 'rgba(255,255,255,0.03)', borderBottom: '1px solid var(--border-color)' }}>
              <tr>
                <th style={{ padding: '1.2rem 1.5rem', fontSize: '0.85rem', color: 'var(--text-muted)' }}>ТОВАР / ВАРИАЦИЯ</th>
                <th style={{ padding: '1.2rem 1.5rem', fontSize: '0.85rem', color: 'var(--text-muted)' }}>ЦЕНА</th>
                <th style={{ padding: '1.2rem 1.5rem', fontSize: '0.85rem', color: 'var(--text-muted)' }}>КОЛИЧЕСТВО</th>
                <th style={{ padding: '1.2rem 1.5rem', fontSize: '0.85rem', color: 'var(--text-muted)' }}>СТАТУС ЗАПАСОВ</th>
                <th style={{ padding: '1.2rem 1.5rem', fontSize: '0.85rem', color: 'var(--text-muted)' }}>ОБНОВЛЕНО</th>
                <th style={{ padding: '1.2rem 1.5rem', fontSize: '0.85rem', color: 'var(--text-muted)' }}></th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr><td colSpan={5} style={{ padding: '4rem', textAlign: 'center' }}>Загрузка данных склада...</td></tr>
              ) : filteredItems.length === 0 ? (
                <tr><td colSpan={5} style={{ padding: '4rem', textAlign: 'center', color: 'var(--text-muted)' }}>Товары не найдены.</td></tr>
              ) : filteredItems.map(item => (
                <tr key={item.sku_id} style={{ borderBottom: '1px solid var(--border-color)' }}>
                  <td style={{ padding: '1.2rem 1.5rem' }}>
                    <div style={{ fontWeight: 'bold' }}>{item.product_title}</div>
                    <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{item.sku_name} (ID: {item.sku_id})</div>
                  </td>
                  <td style={{ padding: '1.2rem 1.5rem' }}>${item.price}</td>
                  <td style={{ padding: '1.2rem 1.5rem' }}>
                    <span style={{ fontSize: '1.1rem', fontWeight: 'bold' }}>{item.quantity} шт.</span>
                  </td>
                  <td style={{ padding: '1.2rem 1.5rem' }}>
                    <StockStatus quantity={item.quantity} />
                  </td>
                  <td style={{ padding: '1.2rem 1.5rem', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                    {new Date(item.updated_at).toLocaleString()}
                  </td>
                  <td style={{ padding: '1.2rem 1.5rem', textAlign: 'right' }}>
                    <button 
                      onClick={() => {
                        addToCart({
                          id: item.sku_id,
                          name: item.sku_name,
                          price: item.price,
                          status: 'ACTIVE',
                          characteristics: []
                        } as any);
                        toast.success('Добавлено в накладную');
                      }}
                      className="glass-btn" 
                    >
                      <PlusCircle size={16} /> Пополнить
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

const StockStatus = ({ quantity }: { quantity: number }) => {
  if (quantity === 0) {
    return <span style={{ color: '#f87171', display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.8rem', fontWeight: 'bold' }}><AlertTriangle size={14} /> НЕТ В НАЛИЧИИ</span>;
  }
  if (quantity < 10) {
    return <span style={{ color: '#fbbf24', display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.8rem', fontWeight: 'bold' }}><AlertTriangle size={14} /> МАЛО</span>;
  }
  return <span style={{ color: '#34d399', display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.8rem', fontWeight: 'bold' }}><Package size={14} /> В НАЛИЧИИ</span>;
};

export default Inventory;

