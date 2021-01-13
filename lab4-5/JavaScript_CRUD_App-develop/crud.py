import json

from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema

with open("secret.json") as f:
    SECRET = json.load(f)

DB_URI = "mysql+mysqlconnector://{user}:{password}@{host}:{port}/{db}".format(
    user=SECRET["user"],
    password=SECRET["password"],
    host=SECRET["host"],
    port=SECRET["port"],
    db=SECRET["db"])

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
db = SQLAlchemy(app)


class Museum(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(30), unique=False)
    visitors = db.Column(db.Integer, unique=False)
    rooms = db.Column(db.Integer, unique=False)

    def __str__(self):
        return f"Name:{self.name} Number of visitors per year:{self.visitors}" \
               f" Number of exhibition-rooms:{self.rooms}  "


class MuseumSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Museum
        sql_session = db.session

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    visitors = fields.Integer(required=True)
    rooms = fields.Integer(required=True)


museum_schema = MuseumSchema()
museums_schema = MuseumSchema(many=True)


@app.route("/home", methods=["GET"])
def get_all_museums():
    all_museums = Museum.query.all()
    museums = museums_schema.dump(all_museums)
    return render_template("index.html", museums=museums)


@app.route("/", methods=["GET", "POST"])
def create_museum():
    if request.method == "POST":
        try:
            museum = Museum(
                name=request.form.get("name"),
                visitors=request.form.get("visitors"),
                rooms=request.form.get("rooms"))

            db.session.add(museum)
            db.session.commit()
            return redirect(url_for('get_all_museums'))
        except Exception as e:
            print("Failed to add museum")
            print(e)

    return render_template("create.html")


@app.route("/update/<id>", methods=["POST", "GET", "PUT"])
def update_museum(id):
    museums = Museum.query.get(id)
    if request.method == "POST":
        if museums.name != request.form["name"]:
            museums.name = request.form["name"]
        if museums.visitors != request.form["visitors"]:
            museums.visitors = request.form["visitors"]
        if museums.rooms != request.form["rooms"]:
            museums.rooms = request.form["rooms"]
        db.session.add(museums)
        db.session.commit()
        return redirect(url_for('get_all_museums'))

    return render_template("edit.html", museums=museums)


@app.route("/delete/<id>")
def delete_museum(id):
    museums = Museum.query.get(id)
    db.session.delete(museums)
    db.session.commit()
    return redirect(url_for('get_all_museums'))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, host="127.0.0.1", port="3000")
