from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import check_password_hash
from a3limni import db
from a3limni.models import User
from a3limni.auth.forms import LoginForm

auth = Blueprint('auth', __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('تم تسجيل الدخول بنجاح!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('فشل تسجيل الدخول. يرجى التحقق من البريد الإلكتروني وكلمة المرور', 'danger')
    
    return render_template('auth/login.html', title='تسجيل الدخول', form=form)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash('تم تسجيل الخروج بنجاح', 'info')
    return redirect(url_for('main.home'))
