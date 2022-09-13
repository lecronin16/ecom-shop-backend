from secrets import token_hex
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

finsta_shop = db.Table('finsta_shop',
    db.Column('cart_id', db.Integer, primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('shop_id', db.Integer, db.ForeignKey('shop.id'))
)

cart = db.Table('cart', 
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('item_id', db.Integer, db.ForeignKey('item.id'))
)

# create our Models based off of our ERD
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    cart = db.relationship("cart",
        secondary = finsta_shop,
        backref = 'buyers',
        lazy = 'dynamic'
    )
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.apitoken = token_hex(16)

    def follow(self, user):
        self.followed.append(user)
        db.session.commit()

    def unfollow(self, user):
        self.followed.remove(user)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'token': self.apitoken
        }
    
    def saveToDB(self):
        db.session.commit()

    def getCart(self):
        list_of_tuples = db.session.query(cart).filter(cart.c.user_id ==self.id).all()
        return [Shop.query.get(t[1]) for t in list_of_tuples]

    def saveToDB(self):
        db.session.commit()

    def addToCart(self, item):
        self.cart.append(item)
        db.session.commit()

    def removeFromCart(self, item):
        self.cart.remove(item)
        db.session.commit()

class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String)
    price = db.Column(db.Integer)
    description = db.Column(db.String)
    img_url = db.Column(db.String)

    def __init__(self, item, price, description, img_url):
        self.item = item
        self.price = price
        self.description = description
        self.img_url = img_url

    def saveItem(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.item,
            'price': self.price,
            'description': self.description,
            'img_url': self.img_url
        }
