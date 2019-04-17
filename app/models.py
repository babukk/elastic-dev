
from sqlalchemy import Table, PrimaryKeyConstraint
from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import InputRequired
from aprmd5 import password_validate

from . import db, app
from . import db_es, metadata_es, engine_es, Base_es


roles_table            = Table('roles', metadata_es, autoload=True, autoload_with=engine_es)
user_company_rel_table = Table('user_company_rel', metadata_es, autoload=True, autoload_with=engine_es)
user_role_rel_table    = Table('user_role_rel', metadata_es, autoload=True, autoload_with=engine_es)


# --------------------------------------------------------------------------------------------------
class Roles(db_es.Model):
    __table__ = roles_table
    __bind_key__ = 'ES'
    __mapper_args__ = {
        'primary_key': roles_table.c.id
    }

    def  __getitem__(self, item):
        return getattr(self, item)


# --------------------------------------------------------------------------------------------------
class UserCompanyRel(db_es.Model):
    __table__ = user_company_rel_table
    __bind_key__ = 'ES'
    __mapper_args__ = {
        'primary_key': user_company_rel_table.c.id
    }

    def  __getitem__(self, item):
        return getattr(self, item)


# --------------------------------------------------------------------------------------------------
class UserRoleRel(db_es.Model):
    __table__ = user_role_rel_table
    __bind_key__ = 'ES'
    __mapper_args__ = {
        'primary_key': user_role_rel_table.c.id
    }

    def  __getitem__(self, item):
        return getattr(self, item)


def checkHtpasswdLogin(htpasswd_file, user, passw):
    try:
        with open(htpasswd_file) as f:
            datafile = f.readlines()
            found = False
            for line in datafile:
                line = line.rstrip("\n\r")
                line = line.rstrip("\n")
                xuser, xhash = line.split(':')
                if user == xuser:
                    if password_validate(passw, xhash):
                        return True
            return False

    except Exception as e:
        print("Error: " + str(e))
        return False


# -------------------------------------------------------------------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))

    def __init__(self, username, password):
        self.username = username

    @staticmethod
    def try_login(username, password):
        # print("FLASK_HTPASSWD_PATH = ", app.config['FLASK_HTPASSWD_PATH'])
        if not checkHtpasswdLogin(app.config['FLASK_HTPASSWD_PATH'], username, password):
            raise ValueError

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def get_username(self):
        return self.username



# --------------------------------------------------------------------------------------------------
class LoginForm(Form):
    username = TextField(u"логин", [InputRequired()])
    password = PasswordField(u"пароль", [InputRequired()])


