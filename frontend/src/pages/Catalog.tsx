import { useState, useEffect } from 'react';
import { productApi } from '../api/products';
import type { Product } from '../api/types';
import ProductCard from '../components/ProductCard';
import { Filter } from 'lucide-react';

const Catalog = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

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

  const filteredProducts = products.filter(p => 
    p.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    p.description?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div style={{ paddingTop: '100px', paddingBottom: '50px' }}>
      <div className="container">
        <header style={{ marginBottom: '3rem', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end' }}>
          <div>
            <h1 style={{ fontSize: '2.5rem', marginBottom: '0.5rem', fontWeight: '800' }}>
              <span className="gradient-text">Каталог</span>
            </h1>
            <p style={{ color: 'var(--text-muted)' }}>Все премиальные товары, доступные для вас.</p>
          </div>
          
          <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
            <div className="glass" style={{ padding: '0.6rem 1rem', borderRadius: '12px', display: 'flex', alignItems: 'center', gap: '0.5rem', width: '300px' }}>
              <Filter size={18} />
              <input 
                type="text" 
                placeholder="Поиск по каталогу..." 
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                style={{ background: 'none', border: 'none', color: 'white', outline: 'none', flex: 1, fontSize: '0.9rem' }}
              />
            </div>
          </div>
        </header>

        {loading ? (
          <div style={{ textAlign: 'center', padding: '5rem' }}>Загрузка коллекции...</div>
        ) : (
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
            gap: '2rem'
          }}>
            {filteredProducts.map(product => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

const MOCK_PRODUCTS: Product[] = [
  {
    id: 1,
    seller_id: 1,
    title: "Quantum Watch Series 7",
    description: "The most advanced wearable technology with holographic display and 7-day battery life.",
    status: "ACTIVE",
    created_at: "",
    updated_at: "",
    skus: [{ id: 1, product_id: 1, seller_id: 1, name: "Standard", price: 499, status: "ACTIVE", characteristics: [] }]
  },
  {
    id: 2,
    seller_id: 1,
    title: "Neural Buds Pro",
    description: "Experience sound like never before with direct neural interface and adaptive noise cancellation.",
    status: "ACTIVE",
    created_at: "",
    updated_at: "",
    skus: [{ id: 2, product_id: 2, seller_id: 1, name: "Standard", price: 299, status: "ACTIVE", characteristics: [] }]
  },
  {
    id: 3,
    seller_id: 2,
    title: "Aura Smart Lamp",
    description: "Mood lighting that synchronizes with your circadian rhythm and health metrics.",
    status: "ACTIVE",
    created_at: "",
    updated_at: "",
    skus: [{ id: 3, product_id: 3, seller_id: 2, name: "Standard", price: 150, status: "ACTIVE", characteristics: [] }]
  },
  {
    id: 4,
    seller_id: 2,
    title: "Zenith Laptop 14\"",
    description: "Ultra-thin, carbon fiber chassis with M3 performance for the ultimate mobile workspace.",
    status: "ACTIVE",
    created_at: "",
    updated_at: "",
    skus: [{ id: 4, product_id: 4, seller_id: 2, name: "Standard", price: 1299, status: "ACTIVE", characteristics: [] }]
  }
];

export default Catalog;

