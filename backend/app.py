from flask import Flask
from flask_cors import CORS
from models import db
from schemas import ma
from routes import routes
from config import Config

app = Flask(__name__)
CORS(app)  # Add this line
app.config.from_object(Config)

db.init_app(app)
ma.init_app(app)

app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80,debug=True)
