from application.database import db
from sqlalchemy import create_engine, Column, Integer, UniqueConstraint, Unicode
from datetime import datetime

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255),nullable=False)
    approved = db.Column(db.Boolean)
    role = db.Column(db.String(255), db.ForeignKey('role.name'))
    cart_ = db.relationship("Cart",backref="user",lazy=True,cascade='all, delete-orphan')
    name = db.Column(db.String(100))
    place=db.Column(db.String)
    age=db.Column(db.Integer)
# Role model
class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

# Category model
class Category(db.Model):
    id=db.Column(db.Integer,autoincrement=True, primary_key=True)
    name=db.Column(db.String(100), unique=True, nullable=False)
    items = db.relationship("Product",backref="category",lazy=True,cascade='all, delete-orphan')
    approved=db.Column(db.Boolean)

# Product model
class Product(db.Model):
    id = db.Column(db.Integer,autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    rate = db.Column(db.Integer,nullable=False)
    quantity = db.Column(db.Integer,nullable=False)
    unit=db.Column(db.String,nullable=False)
    category_id = db.Column(db.Integer,db.ForeignKey("category.id"))
    
class Cart(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    customer_id=db.Column(db.Integer,db.ForeignKey("user.id"))
    item_name=db.Column(db.String(100))
    quantity=db.Column(db.Integer,nullable=False)
    rate=db.Column(db.Integer,nullable=False)

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer)
    amount=db.Column(db.Integer)
    date = db.Column(db.String)