from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"

db = SQLAlchemy(app)

class MailingList(db.Model):
    id = db.Column(db.Integer. primary_key=True)
    adres = db.Column(db.String(120), unique=True, nullable=False)

mail1 = MailingList(adres="akceleratorr@gmail.com")