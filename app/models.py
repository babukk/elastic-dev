
from sqlalchemy import Table, PrimaryKeyConstraint
from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import InputRequired

from . import db, app
from . import db_es, metadata_es, engine_es, Base_es


roles_table            = Table('roles', metadata_es, autoload=True, autoload_with=engine_es)
user_company_rel_table = Table('user_company_rel', metadata_es, autoload=True, autoload_with=engine_es)
user_role_rel_table    = Table('user_role_rel', metadata_es, autoload=True, autoload_with=engine_es)


# --------------------------------------------------------------------------------------------------
class Roles(db.Model):
    __table__ = roles_table
    __bind_key__ = 'ES'
    __mapper_args__ = {
        'primary_key': roles_table.c.id
    }

    def  __getitem__(self, item):
        return getattr(self, item)


# --------------------------------------------------------------------------------------------------
class UserCompanyRel(db.Model):
    __table__ = user_company_rel_table
    __bind_key__ = 'ES'
    __mapper_args__ = {
        'primary_key': user_company_rel_table.c.id
    }

    def  __getitem__(self, item):
        return getattr(self, item)


# --------------------------------------------------------------------------------------------------
class UserRoleRel(db.Model):
    __table__ = user_role_rel_table
    __bind_key__ = 'ES'
    __mapper_args__ = {
        'primary_key': user_role_rel_table.c.id
    }

    def  __getitem__(self, item):
        return getattr(self, item)



# --------------------------------------------------------------------------------------------------
class LoginForm(Form):
    username = TextField(u"логин", [InputRequired()])
    password = PasswordField(u"пароль", [InputRequired()])


