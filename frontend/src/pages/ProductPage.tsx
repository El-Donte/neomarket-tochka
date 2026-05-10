import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ShoppingCart, ArrowLeft, ImageOff, CheckCircle } from 'lucide-react';
import { productApi } from '../api/products';
import type { Product, SKU } from '../api/types';
import { useBuyerCart } from '../store/BuyerCartContext';
import { toast } from 'react-hot-toast';

const ProductPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { addToCart } = useBuyerCart();
  
  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedSku, setSelectedSku] = useState<SKU | null>(null);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const data = await productApi.getById(id || '');
        setProduct(data);
        if (data.skus && data.skus.length > 0) {
          setSelectedSku(data.skus[0]);
        }
      } catch (err) {
        console.error('Failed to fetch product:', err);
        toast.error('Ошибка при загрузке товара');
      } finally {
        setLoading(false);
      }
    };
    if (id) fetchProduct();
  }, [id]);

  const getImageUrl = (url?: string) => {
    if (!url) return null;
    if (url.startsWith('http')) return url;
    const baseUrl = (import.meta.env.VITE_API_URL || 'http://localhost:8080/api/v1').replace('/api/v1', '');
    return `${baseUrl}${url}`;
  };

  const handleAddToCart = () => {
    if (selectedSku) {
      addToCart(selectedSku);
      toast.success(`"${selectedSku.name}" добавлен в корзину`, {
        icon: '🛒',
        style: {
          borderRadius: '10px',
          background: 'var(--bg-secondary)',
          color: '#fff',
        },
      });
    }
  };

  if (loading) {
    return (
      <div style={{ paddingTop: '100px', display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh' }}>
        <div style={{ width: '40px', height: '40px', border: '3px solid var(--accent-primary)', borderTopColor: 'transparent', borderRadius: '50%', animation: 'spin 1s linear infinite' }}></div>
      </div>
    );
  }

  if (!product) {
    return (
      <div style={{ paddingTop: '100px', textAlign: 'center' }}>
        <h2>Товар не найден</h2>
        <button onClick={() => navigate('/catalog')} className="btn-primary" style={{ marginTop: '1rem' }}>В каталог</button>
      </div>
    );
  }

  return (
    <div style={{ paddingTop: '100px', paddingBottom: '50px' }}>
      <div className="container">
        <button 
          onClick={() => navigate(-1)} 
          className="glass-btn" 
          style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '2rem', padding: '0.5rem 1rem' }}
        >
          <ArrowLeft size={18} /> Назад
        </button>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', gap: '4rem', alignItems: 'start' }}>
          {/* Image Section */}
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="glass" 
            style={{ 
              borderRadius: '24px', 
              overflow: 'hidden', 
              aspectRatio: '1', 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center',
              position: 'relative'
            }}
          >
            {product.image_url ? (
              <img 
                src={getImageUrl(product.image_url) || ''} 
                alt={product.title} 
                style={{ width: '100%', height: '100%', objectFit: 'cover' }} 
              />
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', color: 'var(--text-muted)' }}>
                <ImageOff size={64} strokeWidth={1} style={{ marginBottom: '1rem' }} />
                <span>Нет изображения</span>
              </div>
            )}
            {selectedSku && (
              <div style={{ position: 'absolute', top: '20px', right: '20px', background: 'rgba(0,0,0,0.6)', backdropFilter: 'blur(10px)', padding: '0.5rem 1rem', borderRadius: '12px', fontWeight: 'bold', fontSize: '1.2rem', color: 'white', border: '1px solid rgba(255,255,255,0.1)' }}>
                ${selectedSku.price}
              </div>
            )}
          </motion.div>

          {/* Details Section */}
          <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }}>
            <h1 style={{ fontSize: '3rem', fontWeight: '800', marginBottom: '1rem', lineHeight: '1.2' }}>
              <span className="gradient-text">{product.title}</span>
            </h1>
            
            <p style={{ fontSize: '1.1rem', color: 'var(--text-muted)', marginBottom: '2rem', lineHeight: '1.6' }}>
              {product.description || 'Описание отсутствует.'}
            </p>

            {product.skus && product.skus.length > 0 && (
              <div style={{ marginBottom: '3rem' }}>
                <h3 style={{ fontSize: '1.2rem', marginBottom: '1rem', fontWeight: '600' }}>Выберите вариант:</h3>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1rem' }}>
                  {product.skus.map(sku => (
                    <button
                      key={sku.id}
                      onClick={() => setSelectedSku(sku)}
                      style={{
                        padding: '1rem',
                        borderRadius: '16px',
                        border: selectedSku?.id === sku.id ? '2px solid var(--accent-primary)' : '2px solid rgba(255,255,255,0.05)',
                        background: selectedSku?.id === sku.id ? 'rgba(99, 102, 241, 0.1)' : 'rgba(255,255,255,0.03)',
                        color: 'white',
                        cursor: 'pointer',
                        transition: 'all 0.2s ease',
                        display: 'flex',
                        flexDirection: 'column',
                        gap: '0.5rem',
                        minWidth: '120px'
                      }}
                    >
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%' }}>
                        <span style={{ fontWeight: 'bold' }}>{sku.name}</span>
                        {selectedSku?.id === sku.id && <CheckCircle size={16} color="var(--accent-primary)" />}
                      </div>
                      <span style={{ color: 'var(--text-muted)', fontSize: '0.9rem', textAlign: 'left' }}>${sku.price}</span>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {selectedSku && selectedSku.characteristics && selectedSku.characteristics.length > 0 && (
              <div className="glass" style={{ padding: '1.5rem', borderRadius: '16px', marginBottom: '3rem' }}>
                <h4 style={{ marginBottom: '1rem', color: 'var(--text-muted)' }}>Характеристики:</h4>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                  {selectedSku.characteristics.map(char => (
                    <div key={char.id} style={{ display: 'flex', flexDirection: 'column' }}>
                      <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>{char.name}</span>
                      <span style={{ fontWeight: '500' }}>{char.value}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <button 
              onClick={handleAddToCart}
              disabled={!selectedSku}
              className="btn-primary" 
              style={{ width: '100%', padding: '1.2rem', fontSize: '1.1rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.75rem', borderRadius: '16px' }}
            >
              <ShoppingCart size={20} /> В корзину
            </button>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default ProductPage;
