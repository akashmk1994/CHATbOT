import sqlite3


def connect():
    conn = sqlite3.connect("legion.db")
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS legion (task TEXT PRIMARY KEY, date TEXT)")
    conn.commit()
    conn.close()


def add_ent(task_name, date):
    from backend_formfill import cal
    conn = sqlite3.connect("legion.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO legion VALUES (?,?)", (task_name, date))
    conn.commit()
    conn.close()


def view_ent():
    conn = sqlite3.connect("legion.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM legion")
    rows = cur.fetchall()
    conn.close()
    return rows


def delete_ent(task):
    conn = sqlite3.connect("legion.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM legion WHERE task =?", (task,))
    conn.commit()
    conn.close()


connect()
