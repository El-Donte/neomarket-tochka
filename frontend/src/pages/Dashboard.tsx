import { useState, useEffect } from 'react';
import { productApi } from '../api/products';
import apiClient from '../api/client';
import type { ProductDashboardItem } from '../api/types';
import { Plus, Package, Clock, CheckCircle, Edit2, Trash2, Send } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { toast } from 'react-hot-toast';

const Dashboard = () => {
  const [products, setProducts] = useState<ProductDashboardItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [newProduct, setNewProduct] = useState({ 
    title: '', 
    description: '', 
    price: '', 
    sku_name: '', 
    image_url: '',
    characteristics: [] as { name: string, value: string }[]
  });
  const [isUploading, setIsUploading] = useState(false);
  const [activeTab, setActiveTab] = useState<'ALL' | 'MODERATION' | 'PUBLISHED'>('ALL');

  useEffect(() => {
    fetchDashboard(activeTab === 'ALL' ? undefined : activeTab);
  }, [activeTab]);

  const fetchDashboard = async (status?: string) => {
    setLoading(true);
    try {
      const data = await productApi.getDashboard(status);
      setProducts(data);
    } catch (err) {
      console.error('Failed to fetch dashboard:', err);
    } finally {
      setLoading(false);
    }
  };



  const handleEditClick = async (product: ProductDashboardItem) => {
    try {
      const fullProduct = await productApi.getById(product.id);
      const sku = fullProduct.skus?.[0];
      setNewProduct({
        title: fullProduct.title,
        description: fullProduct.description || '',
        image_url: fullProduct.image_url || '',
        price: sku ? sku.price.toString() : '',
        sku_name: sku ? sku.name : '',
        characteristics: sku ? sku.characteristics.map(c => ({ name: c.name, value: c.value })) : []
      });
      setEditingId(product.id);
      setShowAddModal(true);
    } catch (err) {
      toast.error('Не удалось загрузить данные товара');
    }
  };

  const closeModal = () => {
    setShowAddModal(false);
    setEditingId(null);
    setNewProduct({ title: '', description: '', price: '', sku_name: '', image_url: '', characteristics: [] });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (editingId) {
      await handleUpdateProduct();
    } else {
      await handleAddProduct();
    }
  };

  const handleAddProduct = async () => {
    try {
      const product = await productApi.create({
        title: newProduct.title,
        description: newProduct.description,
        image_url: newProduct.image_url
      });

      if (newProduct.price) {
        await apiClient.post(`skus/`, {
          name: newProduct.sku_name || 'Стандарт',
          price: parseFloat(newProduct.price),
          image_url: newProduct.image_url,
          product_id: product.id,
          characteristics: newProduct.characteristics
        });
      }

      toast.success('Товар успешно добавлен!');
      closeModal();
      fetchDashboard();
    } catch (err) {
      console.error('Failed to create product:', err);
      toast.error('Ошибка при создании товара');
    }
  };

  const handleUpdateProduct = async () => {
    try {
      await productApi.update(editingId!, {
        title: newProduct.title,
        description: newProduct.description,
        image_url: newProduct.image_url
      });

      
      const fullProduct = await productApi.getById(editingId!);
      const sku = fullProduct.skus?.[0];

      if (sku) {
        await productApi.updateSku(sku.id, {
          name: newProduct.sku_name || sku.name,
          price: parseFloat(newProduct.price) || sku.price,
        });
      }

      toast.success('Товар обновлен!');
      closeModal();
      fetchDashboard();
    } catch (err) {
      console.error('Update failed:', err);
      toast.error('Ошибка при обновлении товара');
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await apiClient.post('upload/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setNewProduct({ ...newProduct, image_url: response.data.url });
      toast.success('Изображение загружено');
    } catch (err) {
      console.error('Upload failed:', err);
      toast.error('Ошибка при загрузке изображения');
    } finally {
      setIsUploading(false);
    }
  };

  const handleSubmitForModeration = async (id: number) => {
    try {
      await apiClient.post(`products/${id}/submit`);
      toast.success('Товар отправлен на модерацию');
      fetchDashboard();
    } catch (err: any) {
      toast.error(err.response?.data?.detail || 'Ошибка при отправке на модерацию');
    }
  };

  const handleDeleteProduct = async (id: number) => {
    if (!window.confirm('Вы уверены, что хотите удалить этот товар?')) return;
    
    try {
      await productApi.delete(id);
      toast.success('Товар успешно удален');
      fetchDashboard();
    } catch (err: any) {
      console.error('Delete failed:', err);
      toast.error(err.response?.data?.detail || 'Ошибка при удалении товара');
    }
  };

  return (
    <div style={{ paddingTop: '100px', paddingBottom: '50px' }}>
      <div className="container">
        <header style={{ marginBottom: '3rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h1 style={{ fontSize: '2rem', marginBottom: '0.5rem', fontWeight: '800' }}>
              <span className="gradient-text">Дашборд</span>
            </h1>
            <p style={{ color: 'var(--text-muted)' }}>Управляйте своим инвентарем и отслеживайте продажи.</p>
          </div>

          <button onClick={() => setShowAddModal(true)} className="btn-primary" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Plus size={18} /> Добавить товар
          </button>
        </header>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
          gap: '1.5rem',
          marginBottom: '3rem'
        }}>
          <StatCard icon={<Package size={20} />} label="Всего товаров" value={products.length} />
          <StatCard
            icon={<Clock size={20} color="#fbbf24" />}
            label="На модерации"
            value={products.filter(p => p.status === 'ON_MODERATION').length}
          />
          <StatCard
            icon={<CheckCircle size={20} color="#34d399" />}
            label="Опубликовано"
            value={products.filter(p => p.status === 'PUBLISHED').length}
          />
        </div>

        <div style={{ display: 'flex', gap: '1rem', marginBottom: '2rem' }}>
          {(['ALL', 'MODERATION', 'PUBLISHED'] as const).map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className="glass-btn"
              style={{
                background: activeTab === tab ? 'var(--accent-primary)' : 'rgba(255,255,255,0.05)',
                color: activeTab === tab ? 'white' : 'var(--text-muted)',
                border: activeTab === tab ? 'none' : '1px solid var(--border-color)',
                padding: '0.6rem 1.2rem',
                borderRadius: '12px',
                fontWeight: '600'
              }}
            >
              {tab === 'ALL' ? 'Все' : tab === 'MODERATION' ? 'На модерации' : 'Опубликовано'}
            </button>
          ))}
        </div>

        <div className="glass" style={{ borderRadius: 'var(--radius-lg)', overflow: 'hidden' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
            <thead style={{ background: 'rgba(255,255,255,0.03)', borderBottom: '1px solid var(--border-color)' }}>
              <tr>
                <th style={{ padding: '1.2rem 1.5rem', fontSize: '0.85rem', color: 'var(--text-muted)' }}>ТОВАР</th>
                <th style={{ padding: '1.2rem 1.5rem', fontSize: '0.85rem', color: 'var(--text-muted)' }}>СТАТУС</th>
                <th style={{ padding: '1.2rem 1.5rem', fontSize: '0.85rem', color: 'var(--text-muted)' }}>ВАРИАЦИИ</th>
                <th style={{ padding: '1.2rem 1.5rem', fontSize: '0.85rem', color: 'var(--text-muted)' }}>СОЗДАН</th>
                <th style={{ padding: '1.2rem 1.5rem', fontSize: '0.85rem', color: 'var(--text-muted)' }}></th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr><td colSpan={5} style={{ padding: '3rem', textAlign: 'center' }}>Загрузка дашборда...</td></tr>
              ) : products.length === 0 ? (
                <tr><td colSpan={5} style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-muted)' }}>Товары не найдены. Добавьте свой первый товар!</td></tr>
              ) : products.map(product => (
                <tr key={product.id} style={{ borderBottom: '1px solid var(--border-color)', transition: 'var(--transition)' }}>
                  <td style={{ padding: '1.2rem 1.5rem', fontWeight: '600' }}>{product.title}</td>
                  <td style={{ padding: '1.2rem 1.5rem' }}>
                    <StatusBadge status={product.status} />
                  </td>
                  <td style={{ padding: '1.2rem 1.5rem' }}>
                    <span style={{ fontSize: '0.9rem' }}>{product.sku_count} вариантов</span>
                  </td>
                  <td style={{ padding: '1.2rem 1.5rem', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                    {new Date(product.created_at).toLocaleDateString()}
                  </td>
                  <td style={{ padding: '1.2rem 1.5rem', textAlign: 'right' }}>
                    <div style={{ display: 'flex', gap: '0.5rem', justifyContent: 'flex-end' }}>
                      {product.status === 'CREATED' && (
                        <button
                          onClick={() => handleSubmitForModeration(product.id)}
                          className="glass-btn"
                          title="Отправить на модерацию"
                        >
                          <Send size={16} />
                        </button>
                      )}
                      <button
                        onClick={() => handleEditClick(product)}
                        className="glass-btn"
                        title="Редактировать"
                      >
                        <Edit2 size={16} />
                      </button>
                      <button
                        onClick={() => handleDeleteProduct(product.id)}
                        className="glass-btn"
                        style={{ color: '#f87171' }}
                        title="Удалить"
                      >
                        <Trash2 size={16} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <AnimatePresence>
          {showAddModal && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={closeModal}
              style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.8)', backdropFilter: 'blur(8px)', zIndex: 100, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '1rem' }}
            >
              <motion.div
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.9, opacity: 0 }}
                onClick={e => e.stopPropagation()}
                style={{ background: 'var(--bg-secondary)', padding: '2.5rem', borderRadius: '24px', width: '100%', maxWidth: '600px', border: '1px solid var(--border-color)', boxShadow: '0 20px 50px rgba(0,0,0,0.5)', maxHeight: '90vh', overflowY: 'auto' }}
              >
                <h2 style={{ fontSize: '1.8rem', marginBottom: '2rem', fontWeight: '800' }}>
                  <span className="gradient-text">{editingId ? 'Редактировать товар' : 'Добавить товар'}</span>
                </h2>
                <form onSubmit={handleSubmit}>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1rem' }}>
                    <div>
                      <label style={{ display: 'block', fontSize: '0.85rem', marginBottom: '0.5rem', color: 'var(--text-main)' }}>Название товара</label>
                      <input
                        type="text"
                        value={newProduct.title}
                        onChange={e => setNewProduct({ ...newProduct, title: e.target.value })}
                        required
                        style={{ width: '100%', padding: '0.8rem', background: 'rgba(255,255,255,0.05)', border: '1px solid var(--border-color)', borderRadius: '10px', color: 'white' }}
                      />
                    </div>
                    <div>
                      <label style={{ display: 'block', fontSize: '0.85rem', marginBottom: '0.5rem', color: 'var(--text-main)' }}>Название вариации (SKU)</label>
                      <input
                        type="text"
                        placeholder="напр. Черный / XL"
                        value={newProduct.sku_name}
                        onChange={e => setNewProduct({ ...newProduct, sku_name: e.target.value })}
                        style={{ width: '100%', padding: '0.8rem', background: 'rgba(255,255,255,0.05)', border: '1px solid var(--border-color)', borderRadius: '10px', color: 'white' }}
                      />
                    </div>
                  </div>

                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1rem' }}>
                    <div>
                      <label style={{ display: 'block', fontSize: '0.85rem', marginBottom: '0.5rem', color: 'var(--text-main)' }}>Цена ($)</label>
                      <input
                        type="number"
                        value={newProduct.price}
                        onChange={e => setNewProduct({ ...newProduct, price: e.target.value })}
                        required
                        style={{ width: '100%', padding: '0.8rem', background: 'rgba(255,255,255,0.05)', border: '1px solid var(--border-color)', borderRadius: '10px', color: 'white' }}
                      />
                    </div>
                    <div>
                      <label style={{ display: 'block', fontSize: '0.85rem', marginBottom: '0.5rem', color: 'var(--text-main)' }}>Фото товара</label>
                      <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                        <label className="btn-primary" style={{
                          flex: 1,
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          gap: '0.5rem',
                          fontSize: '0.85rem',
                          padding: '0.8rem',
                          cursor: 'pointer',
                          background: 'rgba(255,255,255,0.05)',
                          border: '1px solid var(--border-color)',
                          boxShadow: 'none'
                        }}>
                          <Plus size={18} /> {isUploading ? 'Загрузка...' : 'Загрузить файл'}
                          <input
                            type="file"
                            accept="image/*"
                            onChange={handleFileUpload}
                            style={{ display: 'none' }}
                            disabled={isUploading}
                          />
                        </label>
                        <div style={{ flex: 1 }}>
                          <input
                            type="text"
                            placeholder="или вставьте ссылку"
                            value={newProduct.image_url}
                            onChange={e => setNewProduct({ ...newProduct, image_url: e.target.value })}
                            style={{ width: '100%', padding: '0.8rem', background: 'rgba(255,255,255,0.05)', border: '1px solid var(--border-color)', borderRadius: '10px', color: 'white' }}
                          />
                        </div>
                      </div>
                      {newProduct.image_url && (
                        <div style={{ marginTop: '1rem', height: '100px', borderRadius: '10px', overflow: 'hidden', border: '1px solid var(--border-color)' }}>
                          <img
                            src={newProduct.image_url.startsWith('http') ? newProduct.image_url : (import.meta.env.VITE_API_URL || 'http://localhost:8080/api/v1').replace('/api/v1', '') + newProduct.image_url} 

                            alt="Preview"
                            style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                          />
                        </div>
                      )}
                    </div>
                  </div>

                  <div style={{ marginBottom: '1.5rem' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
                      <label style={{ fontSize: '0.85rem', color: 'var(--text-main)' }}>Характеристики (Размер, Цвет и т.д.)</label>
                      <button 
                        type="button" 
                        onClick={() => setNewProduct({
                          ...newProduct, 
                          characteristics: [...newProduct.characteristics, { name: '', value: '' }]
                        })}
                        style={{ color: '#6366f1', fontSize: '0.85rem', display: 'flex', alignItems: 'center', gap: '0.25rem', background: 'none', border: 'none', cursor: 'pointer' }}
                      >
                        <Plus size={14} /> Добавить
                      </button>
                    </div>
                    
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                      {newProduct.characteristics.map((char, index) => (
                        <div key={index} style={{ display: 'flex', gap: '0.5rem' }}>
                          <input
                            type="text"
                            placeholder="Название (напр. Цвет)"
                            value={char.name}
                            onChange={e => {
                              const newChars = [...newProduct.characteristics];
                              newChars[index].name = e.target.value;
                              setNewProduct({ ...newProduct, characteristics: newChars });
                            }}
                            style={{ flex: 1, padding: '0.6rem', background: 'rgba(255,255,255,0.03)', border: '1px solid var(--border-color)', borderRadius: '8px', color: 'white', fontSize: '0.9rem' }}
                          />
                          <input
                            type="text"
                            placeholder="Значение (напр. Красный)"
                            value={char.value}
                            onChange={e => {
                              const newChars = [...newProduct.characteristics];
                              newChars[index].value = e.target.value;
                              setNewProduct({ ...newProduct, characteristics: newChars });
                            }}
                            style={{ flex: 1, padding: '0.6rem', background: 'rgba(255,255,255,0.03)', border: '1px solid var(--border-color)', borderRadius: '8px', color: 'white', fontSize: '0.9rem' }}
                          />
                          <button 
                            type="button" 
                            onClick={() => {
                              const newChars = newProduct.characteristics.filter((_, i) => i !== index);
                              setNewProduct({ ...newProduct, characteristics: newChars });
                            }}
                            style={{ color: '#f87171', padding: '0 0.5rem', background: 'none', border: 'none', cursor: 'pointer', fontSize: '1.2rem' }}
                          >
                            &times;
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div style={{ marginBottom: '2rem' }}>
                    <label style={{ display: 'block', fontSize: '0.85rem', marginBottom: '0.5rem' }}>Описание</label>
                    <textarea
                      value={newProduct.description}
                      onChange={e => setNewProduct({ ...newProduct, description: e.target.value })}
                      style={{ width: '100%', padding: '0.8rem', background: 'rgba(255,255,255,0.05)', border: '1px solid var(--border-color)', borderRadius: '10px', color: 'white', minHeight: '100px' }}
                    />
                  </div>
                  <div style={{ display: 'flex', gap: '1rem' }}>
                    <button
                      type="button"
                      onClick={closeModal}
                      className="glass-btn"
                      style={{ flex: 1, padding: '1rem' }}
                    >
                      Отмена
                    </button>
                    <button type="submit" className="btn-primary" style={{ flex: 2, padding: '1rem' }}>
                      {editingId ? 'Сохранить изменения' : 'Создать товар'}
                    </button>
                  </div>
                </form>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

const StatCard = ({ icon, label, value }: { icon: any, label: string, value: number }) => (
  <div className="glass" style={{ padding: '1.5rem', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-color)' }}>
    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '0.5rem' }}>
      {icon} {label}
    </div>
    <div style={{ fontSize: '1.8rem', fontWeight: 'bold' }}>{value}</div>
  </div>
);

const StatusBadge = ({ status }: { status: string }) => {
  const colors: Record<string, string> = {
    'CREATED': '#cbd5e1',
    'ON_MODERATION': '#fbbf24',
    'PUBLISHED': '#34d399',
    'REJECTED': '#f87171'
  };
  return (
    <span style={{
      background: `${colors[status] || '#94a3b8'}22`,
      color: colors[status] || '#94a3b8',
      padding: '0.2rem 0.6rem',
      borderRadius: '6px',
      fontSize: '0.75rem',
      fontWeight: 'bold',
      textTransform: 'uppercase'
    }}>
      {status === 'CREATED' ? 'СОЗДАН' :
        status === 'ON_MODERATION' ? 'НА МОДЕРАЦИИ' :
          status === 'PUBLISHED' ? 'ОПУБЛИКОВАН' :
            status === 'REJECTED' ? 'ОТКЛОНЕН' : status}
    </span>
  );
};

export default Dashboard;

