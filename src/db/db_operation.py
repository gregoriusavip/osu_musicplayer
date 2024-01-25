import sqlite3
import logging
import settings
from error_handler import error_handler
from db.error_enum import Error

def isclosed(conn) -> bool:
    """
    A private helper function to check if a connection is closed.

    :param `conn`: a valid connection to an sqlite3 database
    :return: `True` if try block catched an error when establishing cursor to database, `False` otherwise
    """
    try:
        conn.cursor()
        return False
    except Exception as _:
        return True


def create_connection():
    """
    Helper function to establish a connection to an sqlite3 db.
    The name of the database is established on settings.
    Connection need to be manually closed after creating one.

    :return: a valid `sqlite3.connect()` if file is successfully connected, `None` otherwise.
    """
    conn = None
    try:
        conn = sqlite3.connect(settings.DATABASE_NAME)
    except sqlite3.Error as e:
        error_handler(e, "Connect to an sqlite3 db named " + settings.DATABASE_NAME)

    return conn


def create_cursor(conn):
    """
    Helper function to create a cursor to a valid connection
    with a preconfig settings for optimization.
    cursor should be closed after creating one.

    :param `conn`: Valid connection to a database
    :return: an sqlite3 `cursor()` on a valid database, `None` otherwise
    """
    cursor = None
    try:
        cursor = conn.cursor()
        # optimization
        pragma_statements = ["PRAGMA journal_mode = WAL", "PRAGMA synchronous = normal"]
        for statement in pragma_statements:
            cursor.execute(statement)
    except sqlite3.Error as e:
        # Close the connection if an error occurred
        error_handler(e, "Establish a cursor for the database.")
        conn.close()

    return cursor


def add_beatmap(conn, beatmapInfo) -> Error:
    """
    function to add a beatmap info to the database.
    Cursor to the database will be closed after the operation.
    Connection will ONLY be closed if an error occured during data insertion.
    Therefore, connection should be closed if there is no longer operation
    outside of this function.

    :param1 `conn`: connection to a valid database
    :param2 `beatmapInfo`: a dictionary generated from `song_parser.song_parser()`

    :return: enum Error flag. `Error.SUCCESS` if no error occurred, `Error.SQL_EXECUTE_ERROR` otherwise.

    """
    ret = Error.SUCCESS  # return flag
    logging.debug("Current data: " + str(beatmapInfo))
    cursor = create_cursor(conn)
    try:
        insert = """
                    INSERT INTO beatmaps VALUES 
                    (null, :groupID, :BeatmapSetID, :BeatmapID, :Title, :TitleUnicode, :Artist, 
                    :ArtistUnicode, :Creator, :Version, :Source, :Tags, :AudioFilename, :BackgroundFilename, 0)
                """
        cursor.execute(insert, beatmapInfo)
        conn.commit()
    except sqlite3.Error as e:
        # Close the connection if an error occured
        error_handler(
            e, "Failed to add beatmap to the database.\nData: " + str(beatmapInfo)
        )
        ret = Error.SQL_EXECUTE_ERROR
        conn.close()
    finally:
        # Always close the cursor
        cursor.close()

    return ret


def _get_query_top() -> str:
    """
    helper function to get the top part of a default query.
    """
    query = """
            SELECT MAX(CASE
                       WHEN BeatmapSetID IS NOT NULL AND BeatmapSetID <> -1 THEN mainID
                       WHEN BeatmapSetID IS NULL THEN -1
                       ELSE NULL
            END) AS max_mainID,
                groupID, Title, TitleUnicode, Artist, ArtistUnicode, 
                Creator, BeatmapSetID, BackgroundFilename, AudioFilename
            FROM beatmaps
            WHERE HideSong = FALSE
            GROUP BY groupID
            """
    return query

def _execute_query(query: str, user_query=None):
    """
    Execute an SQL query and handle errors
    """
    conn = create_connection()
    if conn is None:
        return Error.SQL_CONNECTION_ERROR
    
    cursor = create_cursor(conn)
    if cursor is None:
        return Error.SQL_ERROR
    
    data = None
    try:
        if user_query is not None or user_query == "":
            cursor.execute(query, ("%" + user_query + "%",))
        else:
            cursor.execute(query)
        data = cursor.fetchall()
    except sqlite3.Error as e:
        # Close the connection if an error occurred
        error_handler(e, "Query: " + query)
    finally:
        cursor.close()
        conn.close()

    if not data:
        return Error.SQL_EXECUTE_ERROR
    return data

def _inject_sort(query: str, sort_by: str):
    """
    inject ORDER BY to a query string and return the query result.
    `ValueError` will be raised if a given sort is not valid.
    """
    sorting_columns={
        "title": "Title",
        "titleunicode": "TitleUnicode",
        "artist": "Artist",
        "artistunicode": "ArtistUnicode"
    }
    lower_sort_by = sort_by.lower()
    if lower_sort_by not in sorting_columns:
        raise ValueError("Invalid sort column specified.")
    
    res_query = query + f" ORDER BY {sorting_columns.get(lower_sort_by)};"
    
    return res_query

def default_select(sort_by: str) -> Error:
    """
    default query, return the result sorted by a given sort

    :return: if an error occured, `SQL_EXECUTE_ERROR`/`SQL_CONNECTION_ERROR`
    otherwise, the result as a `list`
    """
    query = _get_query_top()
    try:
        query = _inject_sort(query, sort_by)
    except Exception as e:
        error_handler(e, "injecting sort")
        return Error.SQL_EXECUTE_ERROR
    return _execute_query(query)

def query_beatmap(user_query: str, sort_by: str) -> Error:
    """
    from a user query, search within the database.
    
    :return: if an error occured, `SQL_EXECUTE_ERROR`/`SQL_CONNECTION_ERROR`
    otherwise, the result as a `list`
    """
    
    query = (_get_query_top()
                + """
                    HAVING (
                        COALESCE(Title, '') || ' ' ||
                        COALESCE(TitleUnicode, '') || ' ' ||
                        COALESCE(Artist, '') || ' ' ||
                        COALESCE(ArtistUnicode, '') || ' ' ||
                        COALESCE(Creator, '') || ' ' ||
                        COALESCE(Version, '') || ' ' ||
                        COALESCE(Source, '') || ' ' ||
                        COALESCE(Tags, '')
                    ) LIKE ?
                """
            )
    try:
        query = _inject_sort(query, sort_by)
    except Exception as e:
        error_handler(e, "injecting sort")
        return Error.SQL_EXECUTE_ERROR
    return _execute_query(query, user_query)