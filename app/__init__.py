from flask import Flask, Blueprint
from config import Config,app_config
#from flask_login import LoginManager
from app.routes import bp

app = Flask(__name__, instance_relative_config=True)
app.register_blueprint(bp)
app.config.from_object(app_config["development"])


def create_app():
    return app
# test_app = Flask(__name__)
# test_app2 = Blueprint ('test_app', __name__)
# test_app.config.from_object (app_config["testing"])


# login = LoginManager (app)
# login.login_view = 'login'


#from app import routes, models
