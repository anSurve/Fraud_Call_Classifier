import sqlite3

connection = sqlite3.connect('database.db')


with open('db_table.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()
cur.execute("INSERT INTO numbers (number) VALUES (?)", ("5912356984",))
cur.execute("INSERT INTO numbers (number) VALUES (?)", ("5912896567",))
cur.execute("INSERT INTO numbers (number, reported_no) VALUES (?, ?)", ("5912896098", 5))
cur.execute("INSERT INTO numbers (number, reported_no) VALUES (?, ?)", ("9812896098", 15))
cur.execute("INSERT INTO numbers (number, reported_no) VALUES (?, ?)", ("9815896098", 12))
cur.execute("INSERT INTO numbers (number, reported_no) VALUES (?, ?)", ("9915696098", 11))
cur.execute("INSERT INTO numbers (number, reported_no) VALUES (?, ?)", ("9917689609", 13))
cur.execute("INSERT INTO numbers (number) VALUES (?)", ("9917897099",))
connection.commit()

cur = connection.cursor()
cur.execute("INSERT INTO submissions (number, filename) VALUES (?, ?)", ("5912356984", "file1.mp3"))
cur.execute("INSERT INTO submissions (number, filename) VALUES (?, ?)", ("5912896567", "file1.mp3"))
cur.execute("INSERT INTO submissions (number, filename) VALUES (?, ?)", ("9812896098", "file3.mp3"))
cur.execute("INSERT INTO submissions (number, filename) VALUES (?, ?)", ("9915696098", "file4.mp3"))
cur.execute("INSERT INTO submissions (number, filename) VALUES (?, ?)", ("9917689609", "file5.mp3"))
cur.execute("INSERT INTO submissions (number, filename) VALUES (?, ?)", ("5912896567", "file6.mp3"))
cur.execute("INSERT INTO submissions (number, filename) VALUES (?, ?)", ("9812896098", "file7.mp3"))
cur.execute("INSERT INTO submissions (number, filename) VALUES (?, ?)", ("9917689609", "file8.mp3"))
connection.commit()
connection.close()
