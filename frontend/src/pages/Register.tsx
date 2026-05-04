import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../store/AuthContext';
import { motion } from 'framer-motion';
import { UserPlus, AlertCircle } from 'lucide-react';
import { toast } from 'react-hot-toast';

const Register = () => {
  const [formData, setFormData] = useState({
    name: '',
    password: '',
    legal_name: '',
    inn: '',
    kpp: ''
  });
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    
    try {
      await register(formData);
      toast.success('Магазин успешно создан!');
      navigate('/');
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Не удалось зарегистрироваться. Пожалуйста, проверьте введенные данные.';
      setError(errorMessage);
      toast.error(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'radial-gradient(circle at bottom left, rgba(99, 102, 241, 0.1), transparent)',
      padding: '2rem'
    }}>
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="glass"
        style={{
          width: '100%',
          maxWidth: '500px',
          padding: '2.5rem',
          borderRadius: 'var(--radius-lg)',
          boxShadow: 'var(--shadow-lg)'
        }}
      >
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <div style={{
            width: '60px',
            height: '60px',
            background: 'var(--accent-primary)',
            borderRadius: '15px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            margin: '0 auto 1rem'
          }}>
            <UserPlus color="white" size={30} />
          </div>
          <h2 style={{ fontSize: '1.8rem', fontWeight: '800' }}>Создать <span className="gradient-text">Магазин</span></h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Присоединяйтесь к NeoMarket и начните продавать сегодня</p>
        </div>

        <form onSubmit={handleSubmit}>
          {error && (
            <div style={{
              background: 'rgba(239, 68, 68, 0.1)',
              color: '#f87171',
              padding: '0.8rem',
              borderRadius: '8px',
              fontSize: '0.85rem',
              marginBottom: '1.5rem',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem'
            }}>
              <AlertCircle size={16} /> {error}
            </div>
          )}

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1.2rem' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', marginBottom: '0.5rem', color: 'var(--text-main)' }}>Полное имя</label>
              <input type="text" name="name" placeholder="Иван Иванов" onChange={handleChange} required className="form-input" />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', marginBottom: '0.5rem', color: 'var(--text-main)' }}>ИНН</label>
              <input type="text" name="inn" placeholder="1234567890" onChange={handleChange} required className="form-input" />
            </div>
          </div>

          <div style={{ marginBottom: '1.2rem' }}>
            <label style={{ display: 'block', fontSize: '0.85rem', marginBottom: '0.5rem', color: 'var(--text-main)' }}>Название организации</label>
            <input type="text" name="legal_name" placeholder="ООО Нео Тех" onChange={handleChange} className="form-input" />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1.2rem' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', marginBottom: '0.5rem', color: 'var(--text-main)' }}>КПП (опционально)</label>
              <input type="text" name="kpp" placeholder="770101001" onChange={handleChange} className="form-input" />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', marginBottom: '0.5rem', color: 'var(--text-main)' }}>Пароль</label>
              <input type="password" name="password" placeholder="••••••••" onChange={handleChange} required className="form-input" />
            </div>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="btn-primary"
            style={{ width: '100%', padding: '0.9rem', fontSize: '1rem', marginTop: '1rem' }}
          >
            {isLoading ? 'Создание аккаунта...' : 'Завершить регистрацию'}
          </button>
        </form>

        <p style={{ textAlign: 'center', marginTop: '1.5rem', fontSize: '0.9rem', color: 'var(--text-muted)' }}>
          Уже есть аккаунт? <Link to="/login" style={{ color: 'var(--accent-secondary)', fontWeight: '600' }}>Войти</Link>
        </p>
      </motion.div>
      
      <style>{`
        .form-input {
          width: 100%;
          padding: 0.8rem 1rem;
          background: rgba(255,255,255,0.05);
          border: 1px solid var(--border-color);
          borderRadius: 10px;
          color: white;
          outline: none;
          transition: var(--transition);
        }
        .form-input:focus {
          border-color: var(--accent-primary);
          background: rgba(255,255,255,0.08);
        }
      `}</style>
    </div>
  );
};

export default Register;

