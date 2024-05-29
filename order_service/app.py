from flask import Flask
from flask_jwt_extended import JWTManager
import configparser

config = configparser.ConfigParser()
config.read("app.ini")
jwt_secret = config["connections"]["JWT_SECRET_KEY"]

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = jwt_secret
jwt = JWTManager(app)

from routes import order_bp
app.register_blueprint(order_bp, url_prefix='/orders')

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5002)
