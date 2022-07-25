from flask import Flask
# import sys
# sys.path.append('c:/Users/victo/Documents/coding projects/coding temple/assignments/unit 5/Car_Place')
from config import Config
from .site.routes import site
from .authentication.routes import auth


from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from models import db as root_db, login_manager, ma
from flask_cors import CORS
from helpers import JSONEncoder

app = Flask(__name__)
CORS(app)

app.register_blueprint(site)
app.register_blueprint(auth)

app.json_encoder = JSONEncoder
app.config.from_object(Config)
root_db.init_app(app)
login_manager.init_app(app)
ma.init_app(app)
migrate = Migrate(app, root_db)
