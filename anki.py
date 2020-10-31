from flask import Flask
from flask import render_template, request
import pandas as pd
import random
from markupsafe import escape
import logging
import sys
import os

root_dir = os.path.dirname(os.path.abspath(__file__))

def create_app():
    myapp = Flask(__name__)
    myapp.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(myapp.instance_path, 'anki_app.sqlite'),
    )
    from anki_app import db
    db.init_app(myapp)
    return myapp

app = create_app()

df = pd.read_csv(os.path.join(root_dir, "words1.csv"))
word = None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/ask')
def ask():
    global word
    the_word = random.choice(df["russ"].tolist())
    word = the_word
    return render_template('ask.html', word=word)

@app.route('/submit', methods=["POST"])
def submit():
    uw = request.form.get('name')
    global word
    correct_bool = False
    cw = df["german"][df["russ"] == word].item()
    try:
        result_word = df["german"][df["german"] == uw].item()
        correct_bool = True
    except:
        print(f"correct is: '{cw}' and user pasted: '{uw}'", file=sys.stderr)
    return render_template('result.html', correct_word=cw, user_word=uw, correct=correct_bool)

