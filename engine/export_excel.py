import pandas as pd
from database.db import get_connection

def export_to_excel(filename="timetable.xlsx"):
    conn = get_connection()

    query = """
    SELECT 
        t.day,
        t.time_slot,
        f.name AS faculty,
        r.name AS room
    FROM timetable t
    JOIN faculty f ON t.faculty_id = f.id
    JOIN room r ON t.room_id = r.id
    """

    df = pd.read_sql(query, conn)
    conn.close()

    df.to_excel(filename, index=False)
