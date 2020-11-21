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
correct_word = None

def get_all_records():
    return Card.query.all()

@app.route('/')
def home():
    return render_template('home.html')

def filter_words(words):
    if correct_word is not None:
        print(f"Correct word: '{correct_word}'")
        russian_word = Card.query.filter_by(gw=correct_word).first().rw
        words.pop(words.index(russian_word))
        print(f"{russian_word} removed from correct words list")
    return words

@app.route('/ask')
def ask():
    global word
    words = get_all_records()
    filtered_words = filter_words([w.rw for w in words])
    if filtered_words:
        the_word = random.choice(filtered_words)
        word = the_word
    else:
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
            global correct_word
            correct_word = cw
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


if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)

