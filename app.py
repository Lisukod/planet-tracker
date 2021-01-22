from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_alembic import Alembic
from flask_mail import Mail, Message
import os, requests, json
from os.path import exists
from pathlib import Path
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = "planet.tracker.py@gmail.com"
app.config["MAIL_PASSWORD"] = "CoolPlanets"
app.config["MAIL_DEFAULT_SENDER"] = "planet.tracker.py@gmail.com"
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True

mail = Mail(app)
db = SQLAlchemy(app)

# Nasa API
url = "https://api.nasa.gov/planetary/apod?api_key=V7p1m6m9yc4K9AJ81pCl95J9bIEEaRpHhMh7b9Bd"

# Check API for updates
def checkNasaAPI():
    if db.session.query(MailingData).first() is None:
        db.session.add(
            MailingData(
                date=datetime.strptime("2000-01-01", "%Y-%m-%d"),
                explanation="Init",
                img="https://picsum.photos/200/300",
                sent=True,
            )
        )
        db.session.commit()
    response = requests.get(url).text
    got_message = json.loads(response)
    date = datetime.strptime(got_message["date"], "%Y-%m-%d")
    db_data = db.session.query(MailingData).first()
    if db_data.date != date:
        db_data.date = date
        db_data.explanation = got_message["explanation"]
        db_data.img = got_message["hdurl"]
        db_data.sent = False
    if db_data.sent == False:
        notify_subs()


scheduler = BackgroundScheduler()
scheduler.add_job(checkNasaAPI, "interval", hours=24)
scheduler.start()


def notify_subs():
    db_data = db.session.query(MailingData).first()
    mailing_list = db.session.query(MailingList).all()
    subscribers = []
    for item in mailing_list:
        subscribers.append(item.adres)
    msg = Message(
        "Hello", 
        recipients=subscribers
    )
    msg.body = db_data.explanation
    mail.send(msg)
    db_data.sent = True
    return "Sent"


class MailingList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    adres = db.Column(db.String(120), unique=True, nullable=False)


class MailingData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=False, nullable=False)
    explanation = db.Column(db.String(240), unique=False, nullable=False)
    img = db.Column(db.String(120), unique=False, nullable=False)
    sent = db.Column(db.Boolean, unique=False, nullable=False)


sess = Session()
sess.init_app(app)


@app.route("/set/")
def set():
    session["key"] = "value"
    return "ok"


@app.route("/get/")
def get():
    return session.get("key", "not set")


@app.route("/")
def main_page():
    return render_template(
        "index.html",
    )


@app.route("/add_to_mailing_list/", methods=["POST"])
def add_mail():
    email_adres = request.form["email"]
    db.session.add(MailingList(adres=email_adres))
    db.session.commit()
    return redirect(url_for("main_page"))

@app.route("/unsubscribe/")
def remove_mail():
    email_adres = ""
    db.session.remove(MailingList(adres=email_adres))
    de.session.commit()




alembic = Alembic()
alembic.init_app(app)
