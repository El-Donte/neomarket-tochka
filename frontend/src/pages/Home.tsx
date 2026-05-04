import { motion } from 'framer-motion';
import { ArrowRight, Star, ShieldCheck, Zap } from 'lucide-react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div style={{ paddingTop: '100px' }}>
      {}
      <section className="container" style={{
        textAlign: 'center',
        minHeight: '80vh',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center'
      }}>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <span style={{
            background: 'rgba(99, 102, 241, 0.1)',
            color: 'var(--accent-secondary)',
            padding: '0.5rem 1rem',
            borderRadius: '20px',
            fontSize: '0.9rem',
            fontWeight: '600',
            marginBottom: '1.5rem',
            display: 'inline-block'
          }}>
            Добро пожаловать в будущее коммерции
          </span>
          <h1 style={{ fontSize: '4rem', fontWeight: '800', lineHeight: '1.1', marginBottom: '1.5rem' }}>
            Улучшайте свой <br />
            <span className="gradient-text">Покупательский опыт</span>
          </h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '1.2rem', maxWidth: '600px', margin: '0 auto 2.5rem' }}>
            Откройте для себя коллекцию премиальных товаров. Быстрая доставка, безопасные платежи и поддержка мирового уровня.
          </p>
          <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', marginTop: '2rem' }}>
            <Link 
              to="/catalog"
              className="btn-primary" 
              style={{ 
                display: 'flex', 
                alignItems: 'center', 
                gap: '0.5rem', 
                textDecoration: 'none',
                padding: '0.8rem 1.8rem',
                borderRadius: 'var(--radius-md)',
                cursor: 'pointer'
              }}
            >
              Каталог товаров <ArrowRight size={18} />
            </Link>
            <Link 
              to="/dashboard"
              style={{
                border: '1px solid var(--border-color)',
                padding: '0.8rem 1.8rem',
                borderRadius: 'var(--radius-md)',
                fontWeight: '600',
                cursor: 'pointer',
                textDecoration: 'none',
                color: 'white',
                display: 'flex',
                alignItems: 'center',
                background: 'rgba(255,255,255,0.05)',
                transition: 'var(--transition)'
              }}
              onMouseEnter={(e) => (e.currentTarget.style.background = 'rgba(255,255,255,0.1)')}
              onMouseLeave={(e) => (e.currentTarget.style.background = 'rgba(255,255,255,0.05)')}
            >
              Портал продавца
            </Link>
          </div>
        </motion.div>
      </section>

      {}
      <section style={{ background: 'var(--bg-secondary)', padding: '5rem 0' }}>
        <div className="container">
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
            gap: '2rem'
          }}>
            <FeatureCard 
              icon={<Zap color="var(--accent-primary)" />} 
              title="Молниеносно" 
              description="Собственная логистическая сеть гарантирует доставку в рекордно короткие сроки."
            />
            <FeatureCard 
              icon={<ShieldCheck color="var(--accent-primary)" />} 
              title="Безопасные платежи" 
              description="Многоуровневое шифрование и защита от мошенничества для каждой транзакции."
            />
            <FeatureCard 
              icon={<Star color="var(--accent-primary)" />} 
              title="Премиальное качество" 
              description="Каждый товар отбирается вручную и проверяется на соответствие самым высоким стандартам."
            />
          </div>
        </div>
      </section>
    </div>
  );
};

const FeatureCard = ({ icon, title, description }: { icon: any, title: string, description: string }) => (
  <motion.div 
    whileHover={{ y: -5 }}
    style={{
      padding: '2rem',
      background: 'var(--bg-primary)',
      borderRadius: 'var(--radius-lg)',
      border: '1px solid var(--border-color)'
    }}
  >
    <div style={{ marginBottom: '1rem' }}>{icon}</div>
    <h3 style={{ marginBottom: '0.5rem' }}>{title}</h3>
    <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>{description}</p>
  </motion.div>
);

export default Home;

