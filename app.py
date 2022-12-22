# URL Shortener using Flask
from flask import Flask
from database import db_session, init_db
from flask_login import LoginManager
from auth import auth as auth_blueprint
from models import User
from main import main as main_blueprint
from flask_mail import Mail


app = Flask(__name__)
app.config['SECRET_KEY'] = 'this should be a secret random string'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'hastingskombe1993@gmail.com'
app.config['MAIL_PASSWORD'] = '227MYk.0120'
app.register_blueprint(auth_blueprint)
app.register_blueprint(main_blueprint)


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
mail = Mail(app)
init_db()


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    app.run(host='0.0.0.0')