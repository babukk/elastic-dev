
from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import func
from sqlalchemy import exc
from aprmd5 import password_validate

from . import app, db, db_es, login_manager
from . models import User, LoginForm


# -------------------------------------------------------------------------------------- / ---------
@app.route('/')
def main_index():

    form = LoginForm(request.form)

    return render_template(
        'index.html',
        form=form,
    )


# ------------------------------------------------------------------------------------ /login ------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash(u"Вы уже вошли на сайт.")
        return redirect("/")

    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            User.try_login(username, password)
        except ValueError:
            flash('Некорректный логин или пароль. Попробуйте повторно войти.', 'danger')
            # return render_template('index.html', form=form)
            return redirect("/")

        user = User.query.filter_by(username=username).first()

        if not user:
            user = User(username, password)
            db.session.add(user)
            db.session.commit()

        login_user(user)
        flash(u"Вы успешно вошли на сайт", "success")
        return redirect("/")

    if form.errors:
        flash(form.errors, 'danger')

    return render_template("index.html", form=form)


# --------------------------------------------------------------------------------------------------
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


# --------------------------------------------------------------------------------- /logout --------
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

