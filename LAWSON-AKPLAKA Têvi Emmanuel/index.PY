from flask import Flask, render_template, request, flash,redirect,url_for
from urllib.parse import quote_plus
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

password = quote_plus('MANUEL')
database_name = 'mabase'
conn = 'postgresql://postgres:{}@localhost:5432/{}'.format(password,database_name)

app.secret_key = 'secret_key'

app.config["SQLALCHEMY_DATABASE_URI"] = conn

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User_et(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    p_word = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True)


with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/acceuil/")
def acceuil():
    return render_template("acceuil.html")

@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        mail = request.form['mail']
        pword = request.form['pass']
        data_1 = User_et.query.filter_by(email=mail).first()

        if data_1 and data_1.p_word == pword:
            return redirect(url_for("acceuil"))
        else:
            flash("Echec de la connexion! Verifier vos informations!!!",category='error')
            flash("Creer un compte si vous n'en avez pas!!!",category='error')
            return render_template("login.html")
    return render_template("login.html")

@app.route("/signup/",methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        nom = request.form['nom']
        prenom = request.form['prenom']
        mail = request.form['mail']
        p_word = request.form['pass']
        cpass = request.form['cpass']
        data_1 = User_et.query.filter_by(email=mail).first()
        if len(nom) < 4:
            flash('Nom doit etre superieur à 3 caractère', category='error')
        elif len(prenom) < 4:
            flash('Prénom doit etre superieur à 3 caractère', category='error')
        elif len(mail) < 6:
            flash('Adreese mail trop court', category='error')
        elif len(p_word) < 7:
            flash('Mot de passe trop court', category='error')
        elif p_word != cpass:
            flash('Mot de passe non conforme', category='error')
        elif data_1:
            flash('Ce email existe déjà', category='error')
        else:
            user = User_et(nom=nom, prenom=prenom, email=mail, p_word=p_word)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("acceuil"))
    return render_template("signup.html")

if __name__=="__main__":
    app.run(debug=True)