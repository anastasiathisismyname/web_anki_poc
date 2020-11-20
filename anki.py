from flask import Flask
from flask import render_template, request
import random
import sys
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"

db = SQLAlchemy(app)

class Card(db.Model):
    __tablename__ = "Card"
    gw = db.Column(db.String)
    rw = db.Column(db.String, primary_key=True)


word = None
words = Card.query.all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/ask')
def ask():
    global word
    the_word = random.choice(words)
    word = the_word.rw
    return render_template('ask.html', word=word)

@app.route('/add_new')
def add_new():
    return render_template('add_new.html', word=word)


@app.route('/delete')
def delete():
    return render_template('delete.html', word=word)


@app.route('/show')
def show():
    return render_template('show.html', rows=words)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
@app.route('/submit', methods=["POST"])
def submit():
    uw = request.form.get('name').lower()
    global word
    correct = False
    cw = Card.query.filter_by(rw=word).first().gw.lower()
    print(f"Correct word: {cw}", file=sys.stderr)
    try:
        uw = Card.query.filter_by(gw=uw).first()
        if uw is not None:
            if uw.gw == cw:
                correct = True
    except:
        print(f"Incorrect input: '{uw}'", file=sys.stderr)
    return render_template('result.html', correct_word=cw, user_word=uw, correct=correct)


@app.route('/add_new_ok', methods=["POST"])
def add_new_ok():
    gw_add = request.form.get('gw').lower()
    rw_add = request.form.get('rw').lower()
    me = Card(gw=gw_add, rw=rw_add)
    db.session.add(me)
    db.session.commit()
    return render_template('home.html')


@app.route('/delete_ok', methods=["POST"])
def delete_ok():
    rus = request.form.get('rw').lower()
    Card.query.filter_by(rw=rus).delete()
    db.session.commit()
    return render_template('home.html')


