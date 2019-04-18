
from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import func
from sqlalchemy import exc
from aprmd5 import password_validate
import json
from pprint import pprint

from . import app, db, db_es, login_manager
from . models import User, LoginForm, UserCompanyRel, UserRoleRel, Roles
from . lib import ElasticSearch

elastic = ElasticSearch.ElasticSearch(host=app.config['ELASTIC_HOST'], port=app.config['ELASTIC_PORT'])


# --------------------------------------------------------------------------------------------------
def getRolesList():
     query = db_es.session.query(Roles)
     result = query.filter(Roles.id != 0).order_by(Roles.id).all()

     return result


# --------------------------------------------------------------------------------------------------
def saveUser2DB(_new_user_id, _role_id, _company_id):
    """ Сохранение отношений user - role, user - company в БД """

    try:
        new_user_company_rel = UserCompanyRel(user_id=_new_user_id, company_id=_company_id)
        db_es.session.add(new_user_company_rel)
        new_user_role_rel = UserRoleRel(user_id=_new_user_id, role_id=_role_id)
        db_es.session.add(new_user_role_rel)
        db_es.session.commit()

    except exc.SQLAlchemyError as e:
        db_es.session.rollback()
        print("saveUser2DB: DB error: " + str(e))


# -------------------------------------------------------------------------------------- / ---------
@app.route('/')
def main_index():

    form = LoginForm(request.form)

    return render_template(
        'index.html',
        form=form,
    )


# -------------------------------------------------------------------------------------- /users ----
@app.route('/users')
@login_required
def users_index():

    form = LoginForm(request.form)

    users_list = elastic.getUsers()
    companies_list = elastic.getCompanies()
    roles_list = getRolesList()
    print("------------------------>> roles_list:")
    print(roles_list)

    return render_template(
        'users.html',
        users_list=users_list,
        companies_list=companies_list,
        roles_list=roles_list,
        form=form,
        page_size=20,
    )


# -------------------------------------------------------------------------------------- /companies -
@app.route('/companies')
@login_required
def companies_index():

    form = LoginForm(request.form)

    companies_list = elastic.getCompanies()
    # print(companies_list)

    return render_template(
        'companies.html',
        companies_list=companies_list,
        form=form,
        page_size=20,
    )


# -------------------------------------------------------------------------------------- /add_company
@app.route('/add_company', methods=['POST'])
def add_company():

    name = request.form['name']
    city = request.form['city']
    email = request.form['email']
    phone = request.form['phone']
    description = request.form['description']

    elastic.addCompany(name=name, city=city, email=email, phone=phone, description=description)

    return json.dumps({'status': 'OK', })


# -------------------------------------------------------------------------------------- /add_user
@app.route('/add_user', methods=['POST'])
def add_user():

    fullname = request.form['fullname']
    email = request.form['email']
    phone = request.form['phone']
    login_name = request.form['login_name']
    description = request.form['description']
    company_id = request.form['company_id']
    role_id = request.form['role_id']
    position = request.form['position']
    description = request.form['description']
    avatar = request.form['avatar']
    passwd = request.form['passwd']

    new_user_id = elastic.addUser(company_id=company_id, fullname=fullname, login=login_name, passwd=passwd,
                                  email=email, phone=phone, position=position, avatar=avatar, description=description)

    saveUser2DB(new_user_id, role_id, company_id)

    return json.dumps({'status': 'OK', })



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

