import flask
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_editable import Editable

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
edit = Editable(app, db)
db.create_all()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/hello", methods=["GET"])
def hello():
    return "Hello"

if __name__ == "__main__":
    app.run()
