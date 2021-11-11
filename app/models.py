from . import db
from flask_login import UserMixin, current_user
from . import login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime, time

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(UserMixin,db.Model):
    ''' class user with its properties '''

    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),unique = True, nullable = False)
    email = db.Column(db.String(255),unique = True, nullable = False)
    pass_secure = db.Column(db.String(255), nullable = False)
    created_at = db.Column(db.DateTime, nullable = False)
    phone_number = db.Column(db.String(10), nullable = True)
    street = db.Column(db.String(80), nullable = True)
    house_number = db.Column(db.String(10), nullable = True)

    @property
    def password(self):
        raise AttributeError('You can not access the password attribute')

    @password.setter
    def password(self,password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()


    def __init__(self, name, email, password, created_at):
        self.name = name
        self.email = email
        self.password = password
        self.created_at = created_at

    def __repr__(self):
        return f'<User {self.email}>'

    
class Menu(db.Model):

    __tablename__ = 'menu'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(255), nullable = False)
    price = db.Column(db.Float, nullable = False)
    type = db.Column(db.String(255), nullable = False)

    def __repr__(self) -> str:
        return f'<User {self.name}>'

class Sell(db.Model):

    __tablename__ = 'sell'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    sell_number = db.Column(db.String(255), nullable = False)
    date = db.Column(db.DateTime, nullable = False, default = datetime.now())
    final_price = db.Column(db.Float, nullable = False)

    def __init__(self, user_id, sell_number, final_price):
        self.user_id = user_id
        self.sell_number = sell_number
        self.final_price = final_price

    def __repr__(self):
        return f'<Sell {self.id}>'

