from flask import Flask
from flask import render_template, request
import random
from markupsafe import escape
import sys
import os
from flask_sqlalchemy import SQLAlchemy
import csv


root_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"

db = SQLAlchemy(app)

class Card(db.Model):
    __tablename__ = "Card"
    gw = db.Column(db.String)
    rw = db.Column(db.String, primary_key=True)


word = None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/ask')
def ask():
    global word
    words = Card.query.all()
    the_word = random.choice(words)
    word = the_word.rw
    return render_template('ask.html', word=word)

@app.route('/submit', methods=["POST"])
def submit():
    uw = request.form.get('name')
    global word
    correct_bool = False
    cw = Card.query.filter_by(rw=word).first().gw
    print(cw, file=sys.stderr)
    try:
        uw = Card.query.filter_by(gw=uw).first()
        if uw is not None:
            if uw.gw == cw:
                correct_bool = True
    except:
        print(f"correct is: '{cw}' and user pasted: '{uw}'", file=sys.stderr)
    return render_template('result.html', correct_word=cw, user_word=uw, correct=correct_bool)

# def main():
#     db.create_all()
#     f = open(os.path.join(root_dir, "words1.csv"))
#     reader = csv.reader(f)
#     for gw, rw in reader:
#         card = Card(gw=gw, rw=rw)
#         db.session.add(card)
#     db.session.commit()
#
# if __name__ == "__main__":
#     with app.app_context():
#         main()