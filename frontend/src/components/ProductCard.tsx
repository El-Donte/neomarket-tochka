import React from 'react';
import { motion } from 'framer-motion';
import { ShoppingCart, Eye, ImageOff } from 'lucide-react';
import { toast } from 'react-hot-toast';
import type { Product } from '../api/types';
import { useCart } from '../store/CartContext';

interface ProductCardProps {
  product: Product;
}

const ProductCard: React.FC<ProductCardProps> = ({ product }) => {
  const { addToCart } = useCart();
  
  
  const sku = product.skus?.[0];
  const price = sku?.price || 0;
  
  const getImageUrl = (url?: string) => {
    if (!url) return null;
    if (url.startsWith('http')) return url;
    
    const baseUrl = (import.meta.env.VITE_API_URL || 'http://localhost:8080/api/v1').replace('/api/v1', '');
    return `${baseUrl}${url}`;
  };

  const handleAddToCart = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (sku) {
      addToCart(sku);
      toast.success(`"${sku.name}" добавлен в корзину`, {
        icon: '🛒',
        style: {
          borderRadius: '10px',
          background: 'var(--bg-secondary)',
          color: '#fff',
        },
      });
    }
  };

  return (
    <motion.div
      whileHover={{ y: -8 }}
      style={{
        background: 'var(--bg-secondary)',
        borderRadius: 'var(--radius-lg)',
        overflow: 'hidden',
        border: '1px solid var(--border-color)',
        display: 'flex',
        flexDirection: 'column'
      }}
    >
        <div style={{ 
          height: '200px', 
          background: 'rgba(255,255,255,0.03)', 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center',
          position: 'relative',
          overflow: 'hidden'
        }}>
          {product.image_url ? (
            <img 
              src={getImageUrl(product.image_url) || ''} 
              alt={product.title} 
              style={{ width: '100%', height: '100%', objectFit: 'cover' }} 
            />
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', color: 'var(--text-muted)', gap: '0.5rem' }}>
              <ImageOff size={40} strokeWidth={1} />
              <span style={{ fontSize: '0.8rem' }}>Нет изображения</span>
            </div>
          )}
          
          {price > 0 && (
            <div style={{ 
              position: 'absolute', 
              bottom: '12px', 
              right: '12px', 
              background: 'var(--accent-primary)', 
              padding: '0.4rem 0.8rem', 
              borderRadius: '8px',
              fontWeight: 'bold',
              boxShadow: '0 4px 12px rgba(0,0,0,0.3)'
            }}>
              ${price}
            </div>
          )}
        </div>
      
      <div style={{ padding: '1.5rem' }}>
        <h3 style={{ fontSize: '1.1rem', marginBottom: '0.5rem' }}>{product.title}</h3>
        <p style={{ 
          color: 'var(--text-muted)', 
          fontSize: '0.85rem', 
          marginBottom: '1.5rem',
          display: '-webkit-box',
          WebkitLineClamp: 2,
          WebkitBoxOrient: 'vertical',
          overflow: 'hidden'
        }}>
          {product.description || 'Описание отсутствует.'}
        </p>
        
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button 
            onClick={handleAddToCart}
            className="btn-primary" 
            style={{ flex: 1, padding: '0.6rem', fontSize: '0.9rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}
          >
            <ShoppingCart size={16} /> Добавить
          </button>
          <button style={{ 
            background: 'rgba(255,255,255,0.05)', 
            padding: '0.6rem', 
            borderRadius: 'var(--radius-md)',
            border: '1px solid var(--border-color)'
          }}>
            <Eye size={18} />
          </button>
        </div>
      </div>
    </motion.div>
  );
};

export default ProductCard;

