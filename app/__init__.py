
import sys
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import exc
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

from config import app_config

app = Flask(__name__, instance_relative_config=True)

app.config.from_object(app_config['development'])
app.config.from_pyfile('config.py')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db = SQLAlchemy(app)
db.init_app(app)

try:
    db.create_all()
except exc.SQLAlchemyError as ex:
    print("Fatal error: " + str(ex))
    sys.exit(1)


engine_es = create_engine(app.config['SQLALCHEMY_BINDS']['DEV_DB'])
Base_es = declarative_base(engine_es)
metadata_es = MetaData(bind=engine_es)

db_es = SQLAlchemy(app, metadata=metadata_es)
db_es.init_app(app)


from . import views, models

# ---------------------------------------------------------------------------------------------------
def create_app(config_name='development'):

    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)

    migrate = Migrate(app, db)

    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"

    Bootstrap(app)

    return app
