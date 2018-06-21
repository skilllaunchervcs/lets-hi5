from flask import Flask
from flask_mongoalchemy import MongoAlchemy

app = Flask(__name__)

app.config['MONGOALCHEMY_DATABASE'] = 'hi5'
app.config['MONGOALCHEMY_CONNECTION_STRING'] = 'mongodb://admin:admin123@ds263520.mlab.com:63520/hi5'

db = MongoAlchemy(app)

class User(db.Document):
    email = db.StringField()
    username = db.StringField()
    password = db.StringField()
    display_picture = db.StringField()

class Posts(db.Document):
    username = db.StringField()
    caption = db.StringField()
    filename = db.StringField()
    category = db.StringField()
    date = db.DateTimeField()
