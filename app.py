from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'biudzetas.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Irasas(db.Model):
    __tablename__ = "irasas"
    id = db.Column(db.Integer, primary_key=True)
    suma = db.Column(db.Float)
    tipas = db.Column(db.String(20))

    def __init__(self, suma, tipas):
        self.suma = abs(suma)
        self.tipas = tipas

    def __repr__(self):
        return f"{self.tipas}: {self.suma}"


with app.app_context():
    db.create_all()


@app.route("/balansas")
def balansas():
    irasai = Irasas.query.all()
    balansas = 0
    for irasas in irasai:
        if irasas.tipas == "pajamos":
            balansas += irasas.suma
        if irasas.tipas == "išlaidos":
            balansas -= irasas.suma
    return render_template("balansas.html", balansas=balansas)


@app.route("/")
def irasai():
    irasai = Irasas.query.all()
    return render_template("index.html", irasai=irasai)


@app.route("/naujas", methods=['GET', 'POST'])
def naujas():
    if request.method == "POST":
        suma = float(request.form['suma'])
        tipas = request.form['tipas']
        irasas = Irasas(suma, tipas)
        db.session.add(irasas)
        db.session.commit()
        return redirect(url_for('naujas'))
    if request.method == "GET":
        return render_template("naujas.html")


if __name__ == "__main__":
    app.run(debug=True)
