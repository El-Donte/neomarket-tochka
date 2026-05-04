import { useState, useEffect } from 'react';
import { invoiceApi } from '../api/invoices';
import type { Invoice } from '../api/invoices';
import { CheckCircle, Clock, ChevronRight, ShoppingBag } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { toast } from 'react-hot-toast';

const Orders = () => {
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedInvoice, setSelectedInvoice] = useState<Invoice | null>(null);
  const [isAccepting, setIsAccepting] = useState(false);

  useEffect(() => {
    fetchInvoices();
  }, []);

  const fetchInvoices = async () => {
    try {
      const data = await invoiceApi.getAll();
      setInvoices(data.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()));
    } catch (err) {
      console.error('Failed to fetch invoices:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleViewDetails = async (id: number) => {
    try {
      const detail = await invoiceApi.getById(id);
      setSelectedInvoice(detail);
    } catch (err) {
      console.error('Failed to fetch invoice detail:', err);
    }
  };

  const handleAccept = async (id: number) => {
    setIsAccepting(true);
    try {
      await invoiceApi.accept(id);
      await fetchInvoices(); 
      setSelectedInvoice(null); 
      toast.success('Накладная успешно принята! Остатки обновлены.');
    } catch (err) {
      console.error('Acceptance failed:', err);
      toast.error('Ошибка при приемке накладной.');
    } finally {
      setIsAccepting(false);
    }
  };

  return (
    <div style={{ paddingTop: '100px', paddingBottom: '50px' }}>
      <div className="container">
        <header style={{ marginBottom: '3rem' }}>
          <h1 style={{ fontSize: '2.5rem', marginBottom: '0.5rem', fontWeight: '800' }}>
            <span className="gradient-text">Накладные</span>
          </h1>
          <p style={{ color: 'var(--text-muted)' }}>Отслеживайте и принимайте поставки товаров на ваш склад.</p>
        </header>

        <div style={{ display: 'grid', gridTemplateColumns: invoices.length > 0 ? '1fr 350px' : '1fr', gap: '2rem' }}>
          {}
          <div className="glass" style={{ borderRadius: 'var(--radius-lg)', overflow: 'hidden' }}>
            {loading ? (
              <div style={{ padding: '4rem', textAlign: 'center' }}>Загрузка накладных...</div>
            ) : invoices.length === 0 ? (
              <div style={{ padding: '4rem', textAlign: 'center', color: 'var(--text-muted)' }}>
                <ShoppingBag size={48} style={{ marginBottom: '1rem', opacity: 0.5 }} />
                <p>Накладные не найдены. Создайте одну в корзине!</p>
              </div>
            ) : (
              <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead style={{ background: 'rgba(255,255,255,0.03)', borderBottom: '1px solid var(--border-color)' }}>
                  <tr>
                    <th style={{ padding: '1.2rem 1.5rem', textAlign: 'left' }}>НОМЕР</th>
                    <th style={{ padding: '1.2rem 1.5rem', textAlign: 'left' }}>СТАТУС</th>
                    <th style={{ padding: '1.2rem 1.5rem', textAlign: 'left' }}>ДАТА</th>
                    <th style={{ padding: '1.2rem 1.5rem', textAlign: 'right' }}>ДЕЙСТВИЕ</th>
                  </tr>
                </thead>
                <tbody>
                  {invoices.map(inv => (
                    <tr 
                      key={inv.id} 
                      onClick={() => handleViewDetails(inv.id)}
                      style={{ 
                        borderBottom: '1px solid var(--border-color)', 
                        cursor: 'pointer',
                        background: selectedInvoice?.id === inv.id ? 'rgba(99, 102, 241, 0.05)' : 'transparent'
                      }}
                    >
                      <td style={{ padding: '1.2rem 1.5rem', fontWeight: 'bold' }}>{inv.number}</td>
                      <td style={{ padding: '1.2rem 1.5rem' }}>
                        <StatusBadge status={inv.status} />
                      </td>
                      <td style={{ padding: '1.2rem 1.5rem', color: 'var(--text-muted)', fontSize: '0.9rem' }}>
                        {new Date(inv.created_at).toLocaleDateString()}
                      </td>
                      <td style={{ padding: '1.2rem 1.5rem', textAlign: 'right' }}>
                        <ChevronRight size={20} color="var(--accent-secondary)" />
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>

          {}
          <AnimatePresence>
            {selectedInvoice && (
              <motion.div 
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                className="glass" 
                style={{ padding: '2rem', borderRadius: 'var(--radius-lg)', height: 'fit-content', position: 'sticky', top: '100px' }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1.5rem' }}>
                  <h2 style={{ fontSize: '1.2rem', color: 'white' }}>Детали: {selectedInvoice.number}</h2>
                  <button onClick={() => setSelectedInvoice(null)} style={{ color: 'white', fontSize: '1.5rem' }}>&times;</button>
                </div>
                
                <div style={{ marginBottom: '2rem' }}>
                  <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>Комментарий:</p>
                  <p style={{ background: 'rgba(255,255,255,0.03)', padding: '0.75rem', borderRadius: '8px', fontSize: '0.9rem' }}>
                    {selectedInvoice.comment || 'Нет комментария'}
                  </p>
                </div>

                <div style={{ marginBottom: '2rem' }}>
                  <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '1rem' }}>Товары:</p>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                    {selectedInvoice.items?.map((item, idx) => (
                      <div key={idx} style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.9rem', borderBottom: '1px solid rgba(255,255,255,0.05)', paddingBottom: '0.5rem' }}>
                        <span>{item.sku_name || `SKU #${item.sku_id}`} <span style={{ color: 'var(--text-muted)' }}>x{item.quantity}</span></span>
                        <span style={{ fontWeight: 'bold' }}>${(item.purchase_price || 0) * item.quantity}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {selectedInvoice.status === 'CREATED' && (
                  <button 
                    onClick={() => handleAccept(selectedInvoice.id)}
                    disabled={isAccepting}
                    className="btn-primary" 
                    style={{ width: '100%', padding: '1rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}
                  >
                    {isAccepting ? 'Обработка...' : <><CheckCircle size={18} /> Принять на склад</>}
                  </button>
                )}
                
                {selectedInvoice.status === 'ACCEPTED' && (
                  <div style={{ 
                    textAlign: 'center', padding: '1rem', background: 'rgba(52, 211, 153, 0.1)', 
                    color: '#34d399', borderRadius: '10px', fontSize: '0.9rem', fontWeight: 'bold',
                    display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem'
                  }}>
                    <CheckCircle size={18} /> Принято, остатки обновлены
                  </div>
                )}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
};

const StatusBadge = ({ status }: { status: string }) => {
  const isAccepted = status === 'ACCEPTED';
  return (
    <span style={{ 
      display: 'inline-flex', alignItems: 'center', gap: '0.4rem',
      background: isAccepted ? 'rgba(52, 211, 153, 0.1)' : 'rgba(251, 191, 36, 0.1)',
      color: isAccepted ? '#34d399' : '#fbbf24',
      padding: '0.3rem 0.75rem',
      borderRadius: '20px',
      fontSize: '0.75rem',
      fontWeight: 'bold'
    }}>
      {isAccepted ? <CheckCircle size={14} /> : <Clock size={14} />}
      {isAccepted ? 'ПРИНЯТО' : 'НОВАЯ'}
    </span>
  );
};

export default Orders;

