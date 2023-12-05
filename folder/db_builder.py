from Error import Error
import sqlite3

def create_db():
    try:
        db = sqlite3.connect("songs.sql")
    except sqlite3.Error as e:
        print('Sql error: %s' % (' '.join(e.args)))
        print("Exception class is: ", e.__class__)
        return Error.SQL_ERROR
    
    db_cur = db.cursor()
    db_cur.execute("DROP TABLE IF EXISTS SONGS")

    table = """ CREATE TABLE SONGS (
                Songsid INTEGER PRIMARY KEY,
                Title TEXT NOT NULL,
                Artist TEXT NOT NULL,
                Repeat BOOLEAN NOT NULL CHECK (Repeat IN (0,1)),
                Path TEXT NOT NULL
            ); """
    
    db_cur.execute(table)
    db_cur.close()
    return Error.SUCCESS
