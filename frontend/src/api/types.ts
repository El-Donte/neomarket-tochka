export type Characteristic = {
  id: string;
  sku_id: string;
  name: string;
  value: string;
};

export type SKU = {
  id: string;
  product_id: string;
  seller_id: string;
  name: string;
  price: number;
  image_url?: string;
  status: string;
  characteristics: Characteristic[];
};

export type Product = {
  id: string;
  seller_id: string;
  category_id?: string;
  title: string;
  image_url?: string;
  description?: string;
  status: string;
  rejection_reason?: string;
  created_at: string;
  updated_at: string;
  skus: SKU[];
};

export type ProductDashboardItem = {
  id: string;
  title: string;
  image_url?: string;
  status: string;
  rejection_reason?: string;
  sku_count: number;
  published_sku_count: number;
  created_at: string;
  updated_at: string;
};

export type ProductCreate = {
  title: string;
  image_url?: string;
  description?: string;
  category_id?: string;
};


