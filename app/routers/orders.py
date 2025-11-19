# routers/orders.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List

from ..database import get_db
from ..models import Order as OrderDB, Item as ItemDB
from ..schemas import Order, OrderCreate, OrderUpdate

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=Order)
def add_order(order: OrderCreate, db: Session = Depends(get_db)):
    """Add an order (purchase)"""
    # Verify item exists and check stock
    item = db.query(ItemDB).filter(ItemDB.id == order.item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    if item.stock_quantity < order.quantity:
        raise HTTPException(status_code=400, detail=f"Not enough stock. Available: {item.stock_quantity}")
    
    # Create order
    unit_price = item.price
    total_amount = unit_price * order.quantity
    
    db_order = OrderDB(
        item_id=order.item_id,
        quantity=order.quantity,
        unit_price=unit_price,
        total_amount=total_amount
    )
    
    # Update stock
    item.stock_quantity -= order.quantity
    
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@router.get("/", response_model=List[Order])
def get_all_orders(db: Session = Depends(get_db)):
    """Get all orders"""
    orders = db.query(OrderDB).all()
    return orders

@router.get("/{order_id}", response_model=Order)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """Get a specific order by ID"""
    db_order = db.query(OrderDB).filter(OrderDB.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.put("/{order_id}", response_model=Order)
def update_order(order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db)):
    """Update an order (quantity, status)"""
    # Fixed: Now properly filtering by order_id
    db_order = db.query(OrderDB).filter(OrderDB.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Handle quantity update
    if order_update.quantity is not None:
        item = db.query(ItemDB).filter(ItemDB.id == db_order.item_id).first()
        if item:
            # Calculate stock change needed
            quantity_diff = order_update.quantity - db_order.quantity
            
            if item.stock_quantity < quantity_diff:
                raise HTTPException(status_code=400, detail="Not enough stock available")
            
            # Update stock and order
            item.stock_quantity -= quantity_diff
            db_order.quantity = order_update.quantity
            db_order.total_amount = db_order.unit_price * order_update.quantity
    
    # Handle status update
    if order_update.status is not None:
        db_order.status = order_update.status
    
    db.commit()
    db.refresh(db_order)
    return db_order

@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    """Delete an order"""
    db_order = db.query(OrderDB).filter(OrderDB.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Restore stock
    item = db.query(ItemDB).filter(ItemDB.id == db_order.item_id).first()
    if item:
        item.stock_quantity += db_order.quantity
    
    db.delete(db_order)
    db.commit()
    return {"message": "Order deleted successfully"}