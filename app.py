from flask import Flask, render_template, request, session
import os
from yourappdb import query_db, get_db
from flask import g

app = Flask(__name__)
app.secret_key="any string"
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
init_db()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def hello_world():
    user = query_db('select * from contacts')
    the_username = "anonyme"
    one_user = query_db('select * from contacts where first_name = ?',
                [the_username], one=True)
    return render_template("hey.html", users=user, one_user=one_user, the_title="my title")
@app.route("/add_one_user", methods=["GET","POST"])
def add_one_user():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into user (username,password,country_id:reference,phone,email) values (:username,:password,:country_id:reference,:phone,:email)",hey)
        user = query_db('select * from user')

        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        session["current_user_id"]=last_user["id"]
        for x in ['username','password','country_id:reference','phone','email']:
            session[x]=hey[x]


        return render_template("userform.html", users=user, one_user=one_user, the_title="add new user")


    user = query_db('select * from user')
    one_user = query_db("select * from user limit 1", one=True)
    return render_template("userform.html", users=user, one_user=one_user, the_title="add new user")


@app.route("/user_sign_out", methods=["GET","POST"])
def user_sign_out():
    if request.method == 'POST':
        session["current_user_id"]=""
        for x in ['username','password','country_id:reference','phone','email']:
            session[x]=""
        return redirect("/")


@app.route("/user_log_in", methods=["GET","POST"])
def user_login():
    if request.method == 'POST':
        hey=request.form
        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        try:
            session["current_user_id"]=last_user["id"]
            for x in ['username','password','country_id:reference','phone','email']:
                session[x]=hey[x]
        except:
            return render_template("userlogin.html")
    return render_template("userlogin.html")
@app.route("/add_one_country", methods=["GET","POST"])
def add_one_country():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into country (name) values (:name)",hey)
        user = query_db('select * from country')

        return render_template("countryform.html", countrys=user, one_user=one_user, the_title="add new country")


    user = query_db('select * from country')
    one_user = query_db("select * from country limit 1", one=True)
    return render_template("countryform.html", countrys=user, one_user=one_user, the_title="add new country")

@app.route("/add_one_domtom", methods=["GET","POST"])
def add_one_domtom():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into domtom (name) values (:name)",hey)
        user = query_db('select * from domtom')

        return render_template("domtomform.html", domtoms=user, one_user=one_user, the_title="add new domtom")


    user = query_db('select * from domtom')
    one_user = query_db("select * from domtom limit 1", one=True)
    return render_template("domtomform.html", domtoms=user, one_user=one_user, the_title="add new domtom")

@app.route("/add_one_domtomhaslanguage", methods=["GET","POST"])
def add_one_domtomhaslanguage():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesdomtom= query_db("select * from domtom")

        tousleslanguage= query_db("select * from language")

        one_user = query_db("insert into domtomhaslanguage (domtom_id,language_id) values (:domtom_id,:language_id)",hey)
        user = query_db('select * from domtomhaslanguage')

        return render_template("domtomhaslanguageform.html", domtomhaslanguages=user, one_user=one_user, the_title="add new domtomhaslanguage", touslesdomtom=touslesdomtom, tousleslanguage=tousleslanguage)


    touslesdomtom= query_db("select * from domtom")

    tousleslanguage= query_db("select * from language")

    user = query_db('select * from domtomhaslanguage')
    one_user = query_db("select * from domtomhaslanguage limit 1", one=True)
    return render_template("domtomhaslanguageform.html", domtomhaslanguages=user, one_user=one_user, the_title="add new domtomhaslanguage", touslesdomtom=touslesdomtom, tousleslanguage=tousleslanguage)

@app.route("/add_one_language", methods=["GET","POST"])
def add_one_language():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into language (name,short_name) values (:name,:short_name)",hey)
        user = query_db('select * from language')

        return render_template("languageform.html", languages=user, one_user=one_user, the_title="add new language")


    user = query_db('select * from language')
    one_user = query_db("select * from language limit 1", one=True)
    return render_template("languageform.html", languages=user, one_user=one_user, the_title="add new language")

@app.route("/add_one_word", methods=["GET","POST"])
def add_one_word():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesfrom_language= query_db("select * from from_language")

        touslesto_language= query_db("select * from to_language")

        one_user = query_db("insert into word (from_language_id,to_language_id,to,word,translation) values (:from_language_id,:to_language_id,:to,:word,:translation)",hey)
        user = query_db('select * from word')

        return render_template("wordform.html", words=user, one_user=one_user, the_title="add new word", touslesfrom_language=touslesfrom_language, touslesto_language=touslesto_language)


    touslesfrom_language= query_db("select * from from_language")

    touslesto_language= query_db("select * from to_language")

    user = query_db('select * from word')
    one_user = query_db("select * from word limit 1", one=True)
    return render_template("wordform.html", words=user, one_user=one_user, the_title="add new word", touslesfrom_language=touslesfrom_language, touslesto_language=touslesto_language)

@app.route("/add_one_sentence", methods=["GET","POST"])
def add_one_sentence():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesfrom_language= query_db("select * from from_language")

        touslesto_language= query_db("select * from to_language")

        one_user = query_db("insert into sentence (from_language_id,to_language_id,content,translation) values (:from_language_id,:to_language_id,:content,:translation)",hey)
        user = query_db('select * from sentence')

        return render_template("sentenceform.html", sentences=user, one_user=one_user, the_title="add new sentence", touslesfrom_language=touslesfrom_language, touslesto_language=touslesto_language)


    touslesfrom_language= query_db("select * from from_language")

    touslesto_language= query_db("select * from to_language")

    user = query_db('select * from sentence')
    one_user = query_db("select * from sentence limit 1", one=True)
    return render_template("sentenceform.html", sentences=user, one_user=one_user, the_title="add new sentence", touslesfrom_language=touslesfrom_language, touslesto_language=touslesto_language)

