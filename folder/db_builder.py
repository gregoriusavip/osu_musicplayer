from scanner import default_scanner
import sqlite3

def create_db():
    if default_scanner():
        db = sqlite3.connect("songs.sql")
    
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
