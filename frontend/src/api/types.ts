export type Characteristic = {
  id: number;
  sku_id: number;
  name: string;
  value: string;
};

export type SKU = {
  id: number;
  product_id: number;
  seller_id: number;
  name: string;
  price: number;
  image_url?: string;
  status: string;
  characteristics: Characteristic[];
};

export type Product = {
  id: number;
  seller_id: number;
  category_id?: number;
  title: string;
  image_url?: string;
  description?: string;
  status: string;
  created_at: string;
  updated_at: string;
  skus: SKU[];
};

export type ProductDashboardItem = {
  id: number;
  title: string;
  image_url?: string;
  status: string;
  sku_count: number;
  published_sku_count: number;
  created_at: string;
  updated_at: string;
};

export type ProductCreate = {
  title: string;
  image_url?: string;
  description?: string;
  category_id?: number;
};


