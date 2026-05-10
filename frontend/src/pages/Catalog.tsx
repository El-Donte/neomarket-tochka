import { useState, useEffect, useMemo } from 'react';
import { productApi } from '../api/products';
import type { Product } from '../api/types';
import ProductCard from '../components/ProductCard';
import { Search, SlidersHorizontal, ChevronDown } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const Catalog = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);

  // Состояния фильтров
  const [searchTerm, setSearchTerm] = useState('');
  const [minPrice, setMinPrice] = useState<string>('');
  const [maxPrice, setMaxPrice] = useState<string>('');
  const [sortOption, setSortOption] = useState<'newest' | 'price_asc' | 'price_desc'>('newest');

  const [showFiltersMobile, setShowFiltersMobile] = useState(false);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const data = await productApi.getAll();
        setProducts(data);
      } catch (error) {
        console.error('Failed to fetch products:', error);
        setProducts(MOCK_PRODUCTS);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  const filteredAndSortedProducts = useMemo(() => {
    let result = products;

    // Поиск
    if (searchTerm) {
      const lowerSearch = searchTerm.toLowerCase();
      result = result.filter(p =>
        p.title.toLowerCase().includes(lowerSearch) ||
        p.description?.toLowerCase().includes(lowerSearch)
      );
    }

    // Фильтр по цене
    if (minPrice || maxPrice) {
      const min = minPrice ? parseFloat(minPrice) : 0;
      const max = maxPrice ? parseFloat(maxPrice) : Infinity;

      result = result.filter(p => {
        const pPrice = p.skus?.[0]?.price || 0;
        return pPrice >= min && pPrice <= max;
      });
    }

    // Сортировка
    result = [...result].sort((a, b) => {
      if (sortOption === 'price_asc') {
        return (a.skus?.[0]?.price || 0) - (b.skus?.[0]?.price || 0);
      }
      if (sortOption === 'price_desc') {
        return (b.skus?.[0]?.price || 0) - (a.skus?.[0]?.price || 0);
      }
      // 'newest' по умолчанию
      return new Date(b.created_at || 0).getTime() - new Date(a.created_at || 0).getTime();
    });

    return result;
  }, [products, searchTerm, minPrice, maxPrice, sortOption]);

  return (
    <div style={{ paddingTop: '100px', paddingBottom: '50px' }}>
      <div className="container">
        <header style={{ marginBottom: '2rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <h1 style={{ fontSize: '2.5rem', marginBottom: '0.5rem', fontWeight: '800' }}>
                <span className="gradient-text">Каталог</span>
              </h1>
              <p style={{ color: 'var(--text-muted)' }}>Найдите идеальный товар среди нашего ассортимента.</p>
            </div>
            <button
              className="glass-btn md-hidden"
              onClick={() => setShowFiltersMobile(!showFiltersMobile)}
              style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', padding: '0.5rem 1rem' }}
            >
              <SlidersHorizontal size={18} /> Фильтры
            </button>
          </div>

          <div className="glass" style={{ padding: '0.8rem 1.5rem', borderRadius: '16px', display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <Search size={20} color="var(--text-muted)" />
            <input
              type="text"
              placeholder="Я ищу..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={{ background: 'none', border: 'none', color: 'white', outline: 'none', flex: 1, fontSize: '1.1rem' }}
            />
          </div>
        </header>

        <div style={{ display: 'grid', gridTemplateColumns: '280px 1fr', gap: '2rem', alignItems: 'start' }} className="catalog-grid">
          {/* Боковая панель фильтров (Фасеты) */}
          <div className={`filters-panel ${showFiltersMobile ? 'show' : ''} glass`} style={{ padding: '1.5rem', borderRadius: 'var(--radius-lg)', position: 'sticky', top: '100px' }}>
            <h3 style={{ fontSize: '1.2rem', fontWeight: 'bold', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <SlidersHorizontal size={18} /> Фасеты
            </h3>

            <div style={{ marginBottom: '2rem' }}>
              <label style={{ display: 'block', fontSize: '0.9rem', marginBottom: '1rem', color: 'var(--text-muted)' }}>Цена ($)</label>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <input
                  type="number"
                  placeholder="От"
                  value={minPrice}
                  onChange={(e) => setMinPrice(e.target.value)}
                  style={{ width: '100%', padding: '0.6rem', background: 'rgba(255,255,255,0.05)', border: '1px solid var(--border-color)', borderRadius: '8px', color: 'white' }}
                />
                <span style={{ color: 'var(--text-muted)' }}>-</span>
                <input
                  type="number"
                  placeholder="До"
                  value={maxPrice}
                  onChange={(e) => setMaxPrice(e.target.value)}
                  style={{ width: '100%', padding: '0.6rem', background: 'rgba(255,255,255,0.05)', border: '1px solid var(--border-color)', borderRadius: '8px', color: 'white' }}
                />
              </div>
            </div>

            <div style={{ marginBottom: '2rem' }}>
              <label style={{ display: 'block', fontSize: '0.9rem', marginBottom: '1rem', color: 'var(--text-muted)' }}>Сортировка</label>
              <div style={{ position: 'relative' }}>
                <select
                  value={sortOption}
                  onChange={(e) => setSortOption(e.target.value as any)}
                  style={{
                    width: '100%',
                    padding: '0.8rem',
                    background: 'rgba(255,255,255,0.05)',
                    border: '1px solid var(--border-color)',
                    borderRadius: '8px',
                    color: 'white',
                    appearance: 'none',
                    outline: 'none',
                    cursor: 'pointer'
                  }}
                >
                  <option value="newest" style={{ background: '#1e1e1e' }}>Сначала новые</option>
                  <option value="price_asc" style={{ background: '#1e1e1e' }}>Сначала дешевые</option>
                  <option value="price_desc" style={{ background: '#1e1e1e' }}>Сначала дорогие</option>
                </select>
                <ChevronDown size={16} style={{ position: 'absolute', right: '12px', top: '50%', transform: 'translateY(-50%)', pointerEvents: 'none', color: 'var(--text-muted)' }} />
              </div>
            </div>

            <button
              onClick={() => {
                setMinPrice('');
                setMaxPrice('');
                setSearchTerm('');
                setSortOption('newest');
              }}
              style={{ width: '100%', padding: '0.8rem', background: 'none', border: '1px solid var(--border-color)', borderRadius: '8px', color: 'var(--text-muted)', cursor: 'pointer', transition: 'all 0.2s ease' }}
              onMouseOver={(e) => e.currentTarget.style.color = 'white'}
              onMouseOut={(e) => e.currentTarget.style.color = 'var(--text-muted)'}
            >
              Сбросить фильтры
            </button>
          </div>

          {/* Сетка товаров */}
          <div>
            <div style={{ marginBottom: '1.5rem', color: 'var(--text-muted)' }}>
              Найдено товаров: <span style={{ color: 'white', fontWeight: 'bold' }}>{filteredAndSortedProducts.length}</span>
            </div>

            {loading ? (
              <div style={{ display: 'flex', justifyContent: 'center', padding: '5rem' }}>
                <div style={{ width: '40px', height: '40px', border: '3px solid var(--accent-primary)', borderTopColor: 'transparent', borderRadius: '50%', animation: 'spin 1s linear infinite' }}></div>
              </div>
            ) : filteredAndSortedProducts.length === 0 ? (
              <div className="glass" style={{ padding: '4rem', textAlign: 'center', borderRadius: 'var(--radius-lg)' }}>
                <p style={{ fontSize: '1.2rem', color: 'var(--text-muted)' }}>По вашему запросу ничего не найдено.</p>
              </div>
            ) : (
              <motion.div
                layout
                style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
                  gap: '2rem'
                }}
              >
                <AnimatePresence>
                  {filteredAndSortedProducts.map(product => (
                    <ProductCard key={product.id} product={product} />
                  ))}
                </AnimatePresence>
              </motion.div>
            )}
          </div>
        </div>
      </div>

      <style>{`
        @media (max-width: 768px) {
          .catalog-grid {
            grid-template-columns: 1fr !important;
          }
          .filters-panel {
            display: none;
          }
          .filters-panel.show {
            display: block;
            position: static !important;
            margin-bottom: 2rem;
          }
          .md-hidden {
            display: flex !important;
          }
        }
        @media (min-width: 769px) {
          .md-hidden {
            display: none !important;
          }
        }
      `}</style>
    </div>
  );
};

const MOCK_PRODUCTS: Product[] = [
  {
    id: "1",
    seller_id: "1",
    title: "Quantum Watch Series 7",
    description: "The most advanced wearable technology with holographic display.",
    status: "ACTIVE",
    created_at: "2026-05-10",
    updated_at: "",
    skus: [{ id: "1", product_id: "1", seller_id: "1", name: "Standard", price: 499, status: "ACTIVE", characteristics: [] }]
  },
  {
    id: "2",
    seller_id: "1",
    title: "Neural Buds Pro",
    description: "Experience sound like never before with direct neural interface.",
    status: "ACTIVE",
    created_at: "2026-05-09",
    updated_at: "",
    skus: [{ id: "2", product_id: "2", seller_id: "1", name: "Standard", price: 299, status: "ACTIVE", characteristics: [] }]
  },
  {
    id: "3",
    seller_id: "2",
    title: "Aura Smart Lamp",
    description: "Mood lighting that synchronizes with your circadian rhythm.",
    status: "ACTIVE",
    created_at: "2026-05-08",
    updated_at: "",
    skus: [{ id: "3", product_id: "3", seller_id: "2", name: "Standard", price: 150, status: "ACTIVE", characteristics: [] }]
  },
  {
    id: "4",
    seller_id: "2",
    title: "Zenith Laptop 14\"",
    description: "Ultra-thin, carbon fiber chassis with M3 performance.",
    status: "ACTIVE",
    created_at: "2026-05-07",
    updated_at: "",
    skus: [{ id: "4", product_id: "4", seller_id: "2", name: "Standard", price: 1299, status: "ACTIVE", characteristics: [] }]
  }
];

export default Catalog;
