from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token,jwt_required
from flask import *
from application.models import db,User,Category,Product,Cart,Purchase
from .cached import get_product
from datetime import timedelta,datetime

#----------------Registeration-------------->

class UserRegister(Resource):
    def post(self):
        # Get the request data
        data = request.get_json()

        if data.get('email') and data.get('password'):
            # Check if the user already exists
            if User.query.filter_by(email=data['email']).first():
                return {'message': 'User already exists'}, 409

            # Create a new user
            user = User(
                email=data['email'],
                password=generate_password_hash(data['password']),
                approved=data['approved'],
                role=data['role']
            )
            db.session.add(user)
            db.session.commit()
            return {'message': 'User registered successfully'}, 201
        else:
            return {'message': 'Missing details'}, 400
        

# <-----------Login Api----------------->

class UserLoginAPI(Resource):
    def post(self):
        #Get the data
        data = request.get_json()

        if data.get('email') and data.get('password'):
            user = User.query.filter_by(email=data['email']).first()
            if user and check_password_hash(user.password, data['password']) and user.approved==True:
                identity = {'id': user.id, 'email': user.email}
                access_token = create_access_token(identity=identity, expires_delta=timedelta(2))
                return {'message': 'User logged in successfully', 'access_token': access_token,'role':user.role,'user_id':user.id}
            return {'message': 'Invalid email or password'}, 401
        else:
            return {'message': 'Missing details'}, 400


#<---------------Category Api----------------------->
class Category_(Resource):
    def post(self):
        data =request.get_json()
        category = Category.query.filter_by(name=data['name']).first()
        if category:
            return {'message':'already exist'},400
        else:
            category_add=Category(
                name=data['name'],
                approved=False
            )
            db.session.add(category_add)
            db.session.commit()
            return {'message':'successfully added'},201
    @jwt_required()
    def get(self):
        category=Category.query.all()
        category_list=[]
        for i in category:
            category_list.append({
                'id':i.id,
                'name':i.name,
                'approved':i.approved
            })
        return jsonify(category_list)
    @jwt_required()
    def put(self):
        data=request.get_json()
        print(data)
        print(data['name'])
        category = Category.query.filter_by(id=data['id']).first()
        if category:
            category.approved= not category.approved
            category.name=data['name']
            db.session.commit()
            return {'message':'Status changed'},201
        else:
            return{'message':'not found'},409
    def delete(self):
        product_id = request.args.get('id')
        category = Category.query.filter_by(id=product_id).first()
        db.session.delete(category)
        db.session.commit()
        return{'message':'successfully deleted'},201

#<------Approve the Managers-------->

class Managers(Resource):
    def get(self):
        managers=User.query.filter_by(role='Manager').all()
        manager_list=[]
        for i in managers:
            manager_list.append({
                'id':i.id,
                'email':i.email,
                'approved':i.approved
            })
        return jsonify(manager_list)
    @jwt_required()
    def put(self):
        data=request.get_json()
        managers=User.query.filter_by(id=data['id']).first()
        if managers:
            managers.approved= not managers.approved
            db.session.commit()
            return {'message':'Status changed'},201
        else:
            return{'message':'not found'},409

class Product_(Resource):
    def post(self):
        data =request.get_json()
        product = Product.query.filter_by(name=data['name']).first()
        if product:
            return {'message':'already exist'},400
        else:
            product_add=Product(
                name=data['name'],
                rate=data['rate'],
                quantity=data['quantity'],
                unit=data['unit'],
                category_id=data['category_id']
            )
            db.session.add(product_add)
            db.session.commit()
            return {'message':'successfully added'},201
    def put(self):
        data =request.get_json()
        i = Product.query.filter_by(id=data['id']).first()
        name1 = data['name']
        rate1 = data['rate']
        quantity1=data['quantity']
        unit1=data['unit']
        category1=data['category_id']
        i.name=name1
        i.rate=rate1
        i.quantity=quantity1
        i.unit=unit1
        i.category_id=category1
        db.session.commit()
    @jwt_required()
    def get(self):
        product=get_product()
        product=Product.query.all()
        product_list=[]
        for i in product:
            product_list.append({
                'id':i.id,
                'name':i.name,
                'rate':i.rate,
                'quantity':i.quantity,
                'unit':i.unit,
                'category_id':i.category_id
            })
        return jsonify(product_list)
    def delete(self):
        product_id = request.args.get('id')
        product=Product.query.filter_by(id=product_id).first()
        db.session.delete(product)
        db.session.commit()
        return {'message': 'Deleted successfully'}, 200
    

#Adding product before cart
class Add_product(Resource):
    def get(self):
        product_id = request.args.get('id')
        product=Product.query.filter_by(id=product_id).first()
        return {
            "name":product.name,"rate":product.rate,'quantity':product.quantity,"unit":product.unit
        } 
    
    def post(self):
        data = request.get_json()
        customer_id = data.get('customer_id')
        quantity = data.get('quantity')

        if not customer_id or not quantity:
            return {'message': 'Missing required parameters'}, 400

        product_id = data.get('product_id')  

        # Check if the product exists
        product = Product.query.get(product_id)
        if not product:
            return {'message': 'Product not found'}, 404

        # Check if the product is in stock
        if product.quantity < quantity:
            return {'message': 'Not enough stock available'}, 400


        # Create a new cart item
        cart_item = Cart(
            customer_id=customer_id,
            item_name=data['item_name'],
            quantity=quantity,
            rate=data['rate']
        )

        # Update the product quantity after adding it to the cart
        product.quantity -= quantity

        # Add the cart item to the database
        db.session.add(cart_item)
        db.session.commit()

        return {'message': 'Item added to the cart successfully'}, 201

#Cart view and delete
class Cart_(Resource):
    def get(self):
        user_id = request.args.get('id')
        cart_items=Cart.query.filter_by(customer_id=user_id).all()
        card_list=[]
        for i in cart_items:
            card_list.append({
                'name':i.item_name,
                'id':i.id,
                'quantity':i.quantity,
                'rate':i.rate,
            })
        return jsonify(card_list)
    def delete(self):
        cart_id = request.args.get('id')
        cart=Cart.query.filter_by(id=cart_id).first()
        product=Product.query.filter_by(name=cart.item_name).first()
        db.session.delete(cart)
        product.quantity=product.quantity+cart.quantity
        db.session.commit()
        return {'message': 'Item added to the cart successfully'}, 200
    def post(self):
        data = request.get_json()
        purchase_item = Purchase(
            customer_id=data['customer_id'],
            amount=data['amount'],
            date=str(datetime.now())
        )
        db.session.add(purchase_item)
        cart=Cart.query.filter_by(customer_id=data['customer_id']).all()
        for i in cart:
            db.session.delete(i)
        db.session.commit()
        return {'message': 'Item added to the Purchased successfully'}, 200 