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


def get_all_records():
    return Card.query.all()

word = None
words = [w.rw for w in get_all_records()]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/ask')
def ask():
    global word
    try:
        the_word = random.choice(words)
        word = the_word
    except IndexError:
        word = None
    return render_template('ask.html', word=word)

@app.route('/add_new')
def add_new():
    return render_template('add_new.html', word=word)

@app.route('/delete')
def delete():
    return render_template('delete.html', word=word)

@app.route('/show')
def show():
    words = get_all_records()
    return render_template('show.html', rows=words)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
@app.route('/submit', methods=["POST"])
def submit():
    global word
    correct = False
    user_input = request.form.get('name')
    if word:
        cw = Card.query.filter_by(rw=word).first().gw.lower()
        print(f"Correct word: '{cw}'", file=sys.stderr)
        uw = user_input.lower().strip()
        print(f"User word: '{uw}'")
        if uw == cw:
            print("Correct!")
            correct = True
            global words
            if words:
                words.pop(words.index(word))
        else:
            print("Incorrect")
        return render_template('result.html', correct_word=cw, user_word=uw, correct=correct)
    return render_template('home.html')

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

@app.route('/refresh')
def refresh():
    global words
    words = [w.rw for w in get_all_records()]
    return render_template('home.html', word=word)


if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)

