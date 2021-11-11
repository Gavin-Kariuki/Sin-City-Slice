from flask import render_template, flash, redirect, url_for, abort, flash, session
from secrets import token_hex
from flask_login import current_user, login_required
from ..models import User, Menu, Sell
from app.auth.views import login, logout
from .. import db,photos, bcrypt
from . import main
from .forms import LocationForm, UserForm

@main.route('/')
def index():
    menu = Menu.query.filter_by(type = 'pizza').all()
    if current_user.is_authenticated:
        user = current_user

    return render_template('index.html', current_user = user, menu = menu)

@main.route('/menu')
def menu():
    menu = Menu.query.filter_by(type = 'pizza').all()
    bei = {product.name : Menu.query.filter_by(name = product.name).first().price for product in menu}
    if current_user.is_authenticated:
        user = current_user

    return render_template('menu.html', current_user = user, menu = menu, prices = bei)

@main.route('profile', methods = ['GET', 'POST'])
@login_required
def user_profile():
    user = current_user
    location_form = LocationForm()
    user_form = UserForm()
    if location_form.submit.data and location_form.validate():
        user.street = location_form.street.data
        user.house_number = location_form.house_number.data
        user.phone_number = location_form.phone_number.data
        #user.save_user()
        db.session.add(user)
        db.session.commit()
        flash('Your profile has been successfully updated')

    elif user_form.submit.data and user_form.validate():
        name = user_form.name.data  
        email = user_form.email.data
        password = user_form.password.data

        if user.name == name and user.email == email and password == '':
            flash('Verify changes please')
            return redirect(url_for('main.user_profile'))

        elif User.query.filter_by(email = email).first() and user.email != email:
            flash(f'The email {email} is already in use')
            return(redirect(url_for('main.user.profile')))

        else:
            user.name = user.name if name == '' else name
            user.email = user.email if email == '' else email
            user.password = user.password if password == '' else bcrypt.generate_password_hash(password)
            db.session.add(user)
            db.session.commit()
            logout()
            flash('Data has been updated')
            return redirect(url_for('main.index'))

    return render_template('main/profile.html', current_user = user, location_form = location_form, user_form = user_form)

@main.route('/about')
def about_us():
    return render_template('main/about.html')

###########################################################
#################CHECKOUT SYSTEM PART######################

@main.route('/cart')
def cart():
    if current_user.is_anonymous:
        return redirect(url_for('auth.login'))

    elif 'cart' not in session:
        session['cart'] = {}

    prices = {k : Menu.query.filter_by(name=k).first().price for k in session['cart'].keys()}
    return render_template('cart.html', cart=session['cart'], prices=prices)

@main.route('/cart/<string:item>')
@main.route('/cart/<string:item>/<int:quantity>')
def add_item(item = '', quantity = 1):
    if current_user.is_anonymous:
        return redirect(url_for('auth.login'))

    if item != '':
        if 'cart' in session:
            cart = session["cart"]
            if item in cart.keys():
                cart[item] += quantity
            else:
                cart[item] = quantity

            session["cart"] = cart

        else:
            session["cart"] = {item : quantity}

        flash('Item has been added successfully')
        return redirect(url_for('cart.cart'))

@main.route('/cart/remove/<string:item')
@login_required
def remove_item(item):
    cart = session.get('cart')
    if cart and item in cart.keys():
        cart.pop(item)
        session['cart'] = cart
        return redirect(url_for('cart.cart'))

    return abort(404)

@main.route('/cart/buy')
@login_required
def buy_item():
    prices = {k : Menu.query.filter_by(name=k).first().price for k in session['cart'].keys()}
    return render_template('buy.html', current_user = current_user, cart = session['cart'], prices = prices)

@main.route('/cart/success', methods = ['GET', 'POST'])
@login_required
def item_success():
    while True:
        sell_number = f'{current_user.street[:2]}-{token_hex(5)}'
        if not Sell.query.filter_by(sell_number = sell_number).first():
            user_id = current_user.id
            final_price = sum([quantity * Menu.query.filter_by(name = product).first().price for product, quantity in session['cart'].items()])
            sell = Sell(user_id, sell_number,final_price)
            db.session.add(sell)
            db.session.commit()
            break

        return render_template('success.html')