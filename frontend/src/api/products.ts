import apiClient from './client';
import type { Product, ProductDashboardItem } from './types';

export const productApi = {
  getAll: async (params?: any) => {
    const response = await apiClient.get<Product[]>('products', { params });
    return response.data;
  },

  getDashboard: async (status?: string) => {
    const response = await apiClient.get<ProductDashboardItem[]>('products/dashboard/', {
      params: { status }
    });
    return response.data;
  },

  getById: async (id: number) => {
    const response = await apiClient.get<Product>(`products/${id}`);
    return response.data;
  },

  create: async (data: any) => {
    const response = await apiClient.post<Product>('products', data);
    return response.data;
  },

  update: async (id: number, data: any) => {
    const response = await apiClient.patch<Product>(`products/${id}`, data);
    return response.data;
  },

  updateSku: async (skuId: number, data: any) => {
    const response = await apiClient.put(`skus/${skuId}`, data);
    return response.data;
  },

  delete: async (id: number) => {
    const response = await apiClient.delete(`products/${id}`);
    return response.data;
  },

  deleteSku: async (skuId: number) => {
    const response = await apiClient.delete(`skus/${skuId}`);
    return response.data;
  }
};

