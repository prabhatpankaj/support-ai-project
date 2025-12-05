import sqlite3


def get_all_tickets(days: int):
    """
    Fetch all support tickets from SQLite database.
    days param unused; included for compatibility.
    """
    conn = sqlite3.connect("db/tickets.db")
    c = conn.cursor()
    c.execute("SELECT id, message FROM tickets")
    rows = c.fetchall()
    conn.close()

    return [{"id": rid, "text": msg} for (rid, msg) in rows]
