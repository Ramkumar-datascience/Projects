import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)

# Create a login manager object
login_manager = LoginManager()



# Often people will also separate these into a separate config.py file
# POSTGRES = {
#     'user': 'postgres',
#     'pw': 'admin',
#     'db': 'CRM',
#     'host': 'localhost',
#     'port': '5432',
# }

app.config['SECRET_KEY'] = 'mysecretkey'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
## app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://DB_USER:PASSWORD@HOST/DATABASE

db = SQLAlchemy(app)
Migrate(app,db)

# We can now pass in our app to the login manager
login_manager.init_app(app)

# Tell users what view to go to when they need to login.
#login_manager.login_view = "login"
@login_manager.user_loader
def load_user(user_id):
	return None
