from flask import Flask
from flask import render_template, request
import pandas as pd
import random
from markupsafe import escape
import logging
import sys
import os

root_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

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
    print(f"user word: {uw}", file=sys.stderr)
    global word
    correct_bool = False
    print(f"question word: {word}", file=sys.stderr)
    cw = df["german"][df["russ"] == word].item()
    try:
        result_word = df["german"][df["german"] == uw].item()
        print(f"result word: {result_word}")
        correct_bool = True
    except:
        print(f"correct is: '{cw}' and user pasted: '{uw}'", file=sys.stderr)
    return render_template('result.html', correct_word=cw, user_word=uw, correct=correct_bool)
