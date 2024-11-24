from flask import Flask
from models import db
from schemas import ma
from routes import routes
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
ma.init_app(app)

app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)
