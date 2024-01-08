# Importing important library
from application.configuration import LocalDevelopmentConfig
from flask import Flask,request,make_response,jsonify
from application.models import Product,User,Role,db,Category,Purchase,Cart
from flask_cors import CORS
from datetime import datetime, timedelta
from workers import celery_init_app
from celery.schedules import crontab
from werkzeug.security import generate_password_hash
import mail
from jinja2 import Template
from flask_restful import Api
from flask_jwt_extended import JWTManager

#intitalizing the Applictaion
app = Flask(__name__)
api = Api(app)
app.config.from_object(LocalDevelopmentConfig)
db.init_app(app)
JWTManager(app)
app.app_context().push()
CORS(app)
celery_app=celery_init_app(app)

#celery job
@celery_app.task()
def daily_reminder():
    with open("./templates/reminder.html","r") as f:   
            template = Template(f.read())
    users = User.query.filter_by(role="END_USER").all()
    # calculate today's date
    today = datetime.now()
    today_str = str(today.strftime("%Y-%m-%d"))
    for user in users:
        today_purchase = Purchase.query.filter(Purchase.date.like(today_str + "%"),Purchase.customer_id==user.id).first()
        if today_purchase:
            mail.send_email(user.email,"Reminder",template.render(user=user.email,list=today_purchase))
        else:
            mail.send_email(user.email,"Reminder",template.render(user=user.email,list=None))

@celery_app.task()
def send_monthly_report():
    # Calculate the start and end of the previous month
    last_month = datetime.now() - timedelta(days=30)
    users = User.query.filter_by(role="END_USER").all()
    for user in users:
        last_month_purchase = Purchase.query.filter(Purchase.date >= last_month,Purchase.customer_id==user.id).all()
        # Create a list of the dates and the number of posts created on each date
        with open("./templates/monthly_report.html","r") as f:   
            template = Template(f.read())
            mail.send_email(user.email,"Monthly report",template.render(orders=last_month_purchase))

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(crontab(minute=12, hour=19), daily_reminder.s(), name='Daily_report')
    #sender.add_periodic_task(10.0, send_monthly_report.s(), name='add every 10')
    sender.add_periodic_task(crontab(00,00, day_of_month='1'), send_monthly_report.s(), name='Monthly_report')

from io import StringIO
import csv
@app.route('/download_products_csv')
def download_products_csv():
    # Query products from the database
    products = Product.query.all()
    # Create a CSV string in memory
    csv_data = StringIO()
    csv_writer = csv.writer(csv_data)
    csv_writer.writerow(['Name', 'Rate', 'Quantity'])  # CSV header

    for product in products:
        csv_writer.writerow([product.name, product.rate, product.quantity])

    # Create a response with the CSV data
    response = make_response(csv_data.getvalue())
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = 'attachment; filename=products.csv'

    return response

from application.api import UserRegister
api.add_resource(UserRegister, '/register')

from application.api import UserLoginAPI
api.add_resource(UserLoginAPI, '/userlogin')

from application.api import Category_
api.add_resource(Category_,'/category')

from application.api import Managers
api.add_resource(Managers,'/managers')

from application.api import Product_
api.add_resource(Product_,'/product')

from application.api import Add_product
api.add_resource(Add_product,'/add_cart')

from application.api import Cart_
api.add_resource(Cart_,'/cart')
#database creation
with app.app_context():
    inspector = db.inspect(db.engine)
    table_names = inspector.get_table_names()

    if not table_names:  # If no tables exist
        db.create_all()
        adminRole = Role(name = 'ADMIN', description = '')
        userRole = Role(name = 'END_USER', description = '')
        managerRole=Role(name = 'Manager', description = '')

        adminUser = User(email="admin@gmail.com",password=generate_password_hash("password"),role="ADMIN",approved=True)
            
        db.session.add(adminRole)
        db.session.add(userRole)
        db.session.add(managerRole)
        db.session.add(adminUser)

        db.session.commit()

        print("Database tables created.")
    else:
        print("Database tables already exist.")

if __name__=="__main__":
    app.run()