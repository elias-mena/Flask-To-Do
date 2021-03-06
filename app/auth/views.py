from flask import render_template, session, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash
from . import auth
from app.forms import LoginForm
from app.firestore_service import get_user, user_put
from app.models import UserModel, UserData

@auth.route('/login', methods=['GET','POST'])
def login():
    login_form = LoginForm()
    context = {
        'login_form': login_form
    }
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        user_doc = get_user(username)

        if user_doc.to_dict() is not None:
            password_from_db = user_doc.to_dict()['password']

            if password == password_from_db:
                user_data = UserData(username, password)
                user = UserModel(user_data)

                login_user(user)

                flash('Bienvenido de nuevo')

                redirect(url_for('hello'))
            else:
                flash('La información no coincide')
        else:
            flash('El usuario no existe')
        return  redirect(url_for('index'))

    return render_template('login.html',**context)

@auth.route('singup', methods=['GET','POST'])
def singup():
    singup_form = LoginForm()
    context = {
        'singup_form':singup_form
    }

    if singup_form.validate_on_submit():
        username = singup_form.username.data
        password = singup_form.password.data

        user_doc = get_user(username)

        if user_doc.to_dict() is None:
            password_hash = generate_password_hash(password)
            user_data = UserData(username, password)
            user_put(user_data)
            user = UserModel(user_data)
            login_user(user)
            flash('Bienvenido')
        else:
            flash('El usuario ya existe')

            return redirect(url_for('hello'))


    return render_template('singup.html',**context)

@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash('Regresa pronto')

    return redirect(url_for('auth.login'))