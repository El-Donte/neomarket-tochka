import React, { createContext, useContext, useState, useEffect } from 'react';
import type { SKU } from '../api/types';

export interface CartItem {
  sku: SKU;
  quantity: number;
}

interface BuyerCartContextType {
  items: CartItem[];
  addToCart: (sku: SKU) => void;
  removeFromCart: (skuId: string) => void;
  updateQuantity: (skuId: string, quantity: number) => void;
  clearCart: () => void;
  totalItems: number;
}

const BuyerCartContext = createContext<BuyerCartContextType | undefined>(undefined);

export const BuyerCartProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [items, setItems] = useState<CartItem[]>(() => {
    const saved = localStorage.getItem('buyer_cart');
    return saved ? JSON.parse(saved) : [];
  });

  useEffect(() => {
    localStorage.setItem('buyer_cart', JSON.stringify(items));
  }, [items]);

  const addToCart = (sku: SKU) => {
    setItems(prev => {
      const existing = prev.find(item => item.sku.id === sku.id);
      if (existing) {
        return prev.map(item =>
          item.sku.id === sku.id ? { ...item, quantity: item.quantity + 1 } : item
        );
      }
      return [...prev, { sku, quantity: 1 }];
    });
  };

  const removeFromCart = (skuId: string) => {
    setItems(prev => prev.filter(item => item.sku.id !== skuId));
  };

  const updateQuantity = (skuId: string, quantity: number) => {
    if (quantity < 1) return;
    setItems(prev =>
      prev.map(item => (item.sku.id === skuId ? { ...item, quantity } : item))
    );
  };

  const clearCart = () => setItems([]);

  const totalItems = items.reduce((sum, item) => sum + item.quantity, 0);

  return (
    <BuyerCartContext.Provider value={{ items, addToCart, removeFromCart, updateQuantity, clearCart, totalItems }}>
      {children}
    </BuyerCartContext.Provider>
  );
};

export const useBuyerCart = () => {
  const context = useContext(BuyerCartContext);
  if (!context) throw new Error('useBuyerCart must be used within a BuyerCartProvider');
  return context;
};
