import csv
import os
from cs50 import SQL
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine(os.environ['DATABASE'])
db = scoped_session(sessionmaker(bind=engine)) 


def main():
    # cargando base de datos desde csv
    f = open("img.csv")
    reader = csv.reader(f, delimiter='#')
    for hexa, name, img, description in reader:
        db.execute("INSERT INTO emojis (hexa, name, img, description) VALUES (:hexa, :name, :img, :description)", {"hexa":hexa, "name": name, "img":img, "description":description})
        print(f"{name}")
    db.commit()

if __name__ == "__main__":
    main()

