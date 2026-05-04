import React, { createContext, useContext, useState, useEffect } from 'react';
import type { SKU } from '../api/types';

interface CartItem {
  sku: SKU;
  quantity: number;
}

interface CartContextType {
  items: CartItem[];
  addToCart: (sku: SKU) => void;
  removeFromCart: (skuId: number) => void;
  updateQuantity: (skuId: number, quantity: number) => void;
  clearCart: () => void;
  totalItems: number;
}

const CartContext = createContext<CartContextType | undefined>(undefined);

export const CartProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [items, setItems] = useState<CartItem[]>([]);

  
  useEffect(() => {
    const savedCart = localStorage.getItem('cart');
    if (savedCart) {
      setItems(JSON.parse(savedCart));
    }
  }, []);

  
  useEffect(() => {
    localStorage.setItem('cart', JSON.stringify(items));
  }, [items]);

  const addToCart = (sku: SKU) => {
    setItems(prev => {
      const existing = prev.find(i => i.sku.id === sku.id);
      if (existing) {
        return prev.map(i => i.sku.id === sku.id ? { ...i, quantity: i.quantity + 1 } : i);
      }
      return [...prev, { sku, quantity: 1 }];
    });
  };

  const removeFromCart = (skuId: number) => {
    setItems(prev => prev.filter(i => i.sku.id !== skuId));
  };

  const updateQuantity = (skuId: number, quantity: number) => {
    if (quantity <= 0) {
      removeFromCart(skuId);
      return;
    }
    setItems(prev => prev.map(i => i.sku.id === skuId ? { ...i, quantity } : i));
  };

  const clearCart = () => setItems([]);

  const totalItems = items.reduce((sum, item) => sum + item.quantity, 0);

  return (
    <CartContext.Provider value={{ items, addToCart, removeFromCart, updateQuantity, clearCart, totalItems }}>
      {children}
    </CartContext.Provider>
  );
};

export const useCart = () => {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error('useCart must be used within a CartProvider');
  }
  return context;
};

