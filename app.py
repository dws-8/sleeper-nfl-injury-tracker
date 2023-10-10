from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'i hope you never guess this'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sleeper_data.db'

db = SQLAlchemy(app)

