from anki import *
import csv
import os

root_dir = os.path.dirname(os.path.abspath(__file__))

def main():
    db.create_all()
    file_data = open(os.path.join(root_dir, "file.csv"))
    reader = csv.reader(file_data)
    for gw, rw in reader:
        card = Card(gw=gw, rw=rw)
        db.session.add(card)
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        main()


# select: print(Card.query.filter_by(rw="russian").first().gw)
# delete: Card.query.filter_by(rw="как мне добраться до больницы Элизабет").delete()