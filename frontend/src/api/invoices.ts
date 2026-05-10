import apiClient from './client';

export interface InvoiceItem {
  sku_id: number;
  quantity: number;
  purchase_price: number;
  sku_name?: string;
  sku_price?: number;
}

export interface Invoice {
  id: string;
  seller_id: string;
  number: string;
  status: 'CREATED' | 'ACCEPTED';
  comment?: string;
  created_at: string;
  updated_at: string;
  items?: InvoiceItem[];
}

export const invoiceApi = {
  getAll: async () => {
    const response = await apiClient.get<Invoice[]>('invoices/');
    return response.data;
  },
  
  getById: async (id: string) => {
    const response = await apiClient.get<Invoice>(`invoices/${id}`);
    return response.data;
  },
  
  create: async (data: { number: string; comment?: string; items: InvoiceItem[] }) => {
    const response = await apiClient.post<Invoice>('invoices/', data);
    return response.data;
  },
  
  accept: async (id: string) => {
    const response = await apiClient.post<Invoice>(`invoices/accept?invoice_id=${id}`);
    return response.data;
  }
};

