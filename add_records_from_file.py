from main import *
import csv
import os

root_dir = os.path.dirname(os.path.abspath(__file__))

def add_from_file():
    db.create_all()
    file_data = open(os.path.join(root_dir, "file.csv"))
    reader = csv.reader(file_data)
    for gw, rw in reader:
        card = Card(gw=gw, rw=rw)
        db.session.add(card)
    db.session.commit()

def update_word():
    to_update = Card.query.filter_by(gw="später").first()
    to_update.rw = "позже"
    db.session.commit()


def delete_all_words():
    all = Card.query.all()
    for w in all:
        Card.query.filter_by(rw=w.rw).delete()
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        delete_all_words()


# select: print(Card.query.filter_by(rw="russian").first().gw)
# delete: Card.query.filter_by(rw="как мне добраться до больницы Элизабет").delete()