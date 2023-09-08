from flask import Flask, render_template, redirect, url_for, request
import sqlite3 as db
import re
import random
import os
from flask_sqlalchemy import SQLAlchemy


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Product(db.Model):
    id= db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(100), primary_key=True)
    stock_on_hand = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Title: {}>".format(self.product_name)



@app.route('/',methods=['GET','POST']) 

def index():
    db.create_all()
    if request.method=='POST':
       value1=request.form.get('one')
       value2=request.form.get('two')
       value3=request.form.get('three')
       value4=request.form.get('four')
       value5=request.form.get('five')
       value6=request.form.get('x')
       print(value2)
       if(value1):
           number=0
           x=Product.query.all()
           x=list(x)
           number=len(x)
           for i in range(number,number+50):
               n="item"+" "+str(i)
               stock=random.randint(20,50)
               product = Product(product_name=n,stock_on_hand=stock)
               db.session.add(product)
               db.session.commit()
           return render_template('index.html')
       
       elif(value2):
           per_page=20
           page = request.args.get('page',1, type=int)
           pagination = Product.query.order_by(Product.product_name).paginate(page=page, per_page=per_page)
           return render_template("result1.html",pagination=pagination)
       
       elif(value3):
           per_page=20
           page = request.args.get('page',1, type=int)
           pagination = Product.query.order_by(Product.stock_on_hand.desc()).paginate(page=page, per_page=per_page)
           return render_template("result.html",pagination=pagination)
       
       elif(value4):
           per_page=20
           page = request.args.get('page',1, type=int)
           v=Product.query.all()
           for i in v:
               k=i.product_name
               m=i.stock_on_hand
               print(m)
               if(m-2>=0):
                   i.stock_on_hand=m-2
                   db.session.commit()
           pagination = Product.query.order_by(Product.id).paginate(page=page, per_page=per_page)
           return render_template("product.html",pagination=pagination)
       
       elif(value5):
           v=Product.query.all()
           for i in v:
               k=i.product_name
               m=i.stock_on_hand
               k=str(k)
               k=k.split(" ")
               k=k[1]
               k=int(k)
               if(k%2==0):
                   i.stock_on_hand=m+2
                   db.session.commit()

           per_page=20
           page = request.args.get('page',1, type=int)
           pagination = Product.query.order_by(Product.id).paginate(page=page, per_page=per_page)
           return render_template("product.html",pagination=pagination)
       
           
       elif(value6):
           per_page=20
           page = request.args.get('page',1, type=int)
           pagination = Product.query.order_by(Product.id).paginate(page=page, per_page=per_page)
           return render_template("product.html",pagination=pagination)
       
           
    return render_template('index.html')

@app.route('/v', methods=['GET'], defaults={"page": 1})
@app.route('/v/page=<int:page>', methods=['GET'])
def val(page):
    per_page=20
    url = request.path
    url=str(url)
    
    if("=" in url):
        url=url.split("=")
        page=url[1]
        page=int(page)
    else:
        page=1

    pagination = Product.query.order_by(Product.id).paginate(page=page, per_page=per_page)
    return render_template("product.html",pagination=pagination)

@app.route('/asc', methods=['GET'], defaults={"page": 1})
@app.route('/asc/page=<int:page>', methods=['GET'])
def asc(page):
    per_page=20
    url = request.path
    url=str(url)
    
    if("=" in url):
        url=url.split("=")
        page=url[1]
        page=int(page)
    else:
        page=1

    pagination = Product.query.order_by(Product.product_name).paginate(page=page, per_page=per_page)
    return render_template("result1.html",pagination=pagination)

@app.route('/desc', methods=['GET'], defaults={"page": 1})
@app.route('/desc/page=<int:page>', methods=['GET'])
def desc(page):
    per_page=20
    url = request.path
    url=str(url)
    
    if("=" in url):
        url=url.split("=")
        page=url[1]
        page=int(page)
    else:
        page=1

    pagination = Product.query.order_by(Product.stock_on_hand.desc()).paginate(page=page, per_page=per_page)
    return render_template("result.html",pagination=pagination)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8000)