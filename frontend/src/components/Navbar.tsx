import { Link } from 'react-router-dom';
import { ShoppingBag, Search, LogOut } from 'lucide-react';
import { useAuth } from '../store/AuthContext';
import { useCart } from '../store/CartContext';
import { useBuyerCart } from '../store/BuyerCartContext';

const Navbar = () => {
  const { user, logout } = useAuth();
  const { totalItems: supplyItems } = useCart();
  const { totalItems: buyerItems } = useBuyerCart();

  return (
    <nav className="glass" style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      zIndex: 1000,
      height: '70px',
      display: 'flex',
      alignItems: 'center',
      padding: '0 2rem'
    }}>
      <div className="container" style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        width: '100%'
      }}>
        <Link to="/" style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>
          Neo<span className="gradient-text">Market</span>
        </Link>

        <div style={{ display: 'flex', gap: '2rem', alignItems: 'center' }}>
          <div className="search-bar" style={{
            background: 'rgba(255,255,255,0.05)',
            padding: '0.5rem 1rem',
            borderRadius: '20px',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem'
          }}>
            <Search size={18} color="var(--text-muted)" />
            <input 
              type="text" 
              placeholder="Поиск товаров..." 
              style={{ background: 'none', border: 'none', color: 'white', outline: 'none' }}
            />
          </div>
          
          <Link to="/catalog">Каталог</Link>
          {user && <Link to="/dashboard">Дашборд</Link>}
          {user && <Link to="/inventory">Инвентарь</Link>}
          {user && <Link to="/orders">Накладные</Link>}
          <Link to="/buyer-cart" style={{ position: 'relative', display: 'flex', alignItems: 'center', gap: '0.4rem', color: 'white' }}>
            <ShoppingBag size={20} />
            <span style={{ fontSize: '0.95rem' }}>Корзина</span>
            {buyerItems > 0 && (
              <span style={{
                position: 'absolute',
                top: '-8px',
                right: '-8px',
                background: 'var(--accent-primary)',
                color: 'white',
                fontSize: '0.7rem',
                width: '18px',
                height: '18px',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontWeight: 'bold',
                boxShadow: '0 2px 4px rgba(0,0,0,0.3)'
              }}>
                {buyerItems}
              </span>
            )}
          </Link>
          {user && <Link to="/buyer-orders">Мои заказы</Link>}

          {user && (
          <Link to="/cart" style={{ position: 'relative', display: 'flex', alignItems: 'center', gap: '0.4rem', marginLeft: '1rem', paddingLeft: '1rem', borderLeft: '1px solid rgba(255,255,255,0.1)' }}>
            <span style={{ fontSize: '0.95rem', color: 'var(--text-muted)' }}>Поставка</span>
            {supplyItems > 0 && (
              <span style={{
                position: 'absolute',
                top: '-8px',
                right: '-8px',
                background: '#fbbf24',
                color: 'black',
                fontSize: '0.7rem',
                width: '18px',
                height: '18px',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontWeight: 'bold'
              }}>
                {supplyItems}
              </span>
            )}
          </Link>
          )}
          
          {user ? (
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <div style={{ 
                  width: '32px', 
                  height: '32px', 
                  background: 'var(--accent-primary)', 
                  borderRadius: '50%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '0.8rem',
                  fontWeight: 'bold'
                }}>
                  {user.name.charAt(0).toUpperCase()}
                </div>
                <span style={{ fontSize: '0.9rem', fontWeight: '500' }}>{user.name}</span>
              </div>
              <button onClick={logout} style={{ color: 'var(--text-muted)' }}>
                <LogOut size={20} />
              </button>
            </div>
          ) : (
            <Link to="/login" className="btn-primary" style={{ padding: '0.5rem 1.2rem' }}>
              Войти
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;

