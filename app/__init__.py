from flask import Flask
from app.models import db
from app.controllers import main
from app.controllers import movies
from app.controllers import reviews
from prefixmid import PrefixMiddleware

app = Flask(__name__, template_folder='static/site', static_url_path="/static", static_folder="static")

app.config.from_object('config.Config')
app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix='/juan')
db.init_app(app)
db.create_all(app=app)


app.register_blueprint(main, url_prefix='/')
app.register_blueprint(movies, url_prefix='/movies')
app.register_blueprint(reviews, url_prefix='/reviews')

