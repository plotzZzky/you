from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


UPLOAD_FOLDER = 'static/uploaded_files'
ALLOWED_EXTENSIONS = {'png', 'webp', 'jpeg', 'jpg'}


app = Flask(__name__)
app.config['SECRET_KEY'] = '192b9bdd22ab9ed4d12e236c78afcb9a393easssk9jhsbsbsusu82828s8j8sjs8s'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres@localhost:5432/you"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

login_manager = LoginManager(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'login'
login_manager.init_app(app)

db = SQLAlchemy(app)
