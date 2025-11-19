# schemas.py
from pydantic import BaseModel
from typing import Optional

# Category schemas
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    
    class Config:
        from_attributes = True

# Item schemas
class ItemBase(BaseModel):
    name: str
    description: str
    price: float
    stock_quantity: int
    category_id: Optional[int] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    category: Optional[Category] = None
    
    class Config:
        from_attributes = True

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None
    category_id: Optional[int] = None

# Order schemas
class OrderBase(BaseModel):
    item_id: int
    quantity: int

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    quantity: Optional[int] = None
    status: Optional[str] = None

class Order(OrderBase):
    id: int
    unit_price: float
    total_amount: float
    status: str
    
    class Config:
        from_attributes = True
