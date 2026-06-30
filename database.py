import sqlite3

def create_table():

    conn = sqlite3.connect("data/council.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS decisions (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        question TEXT,
        
        risk INTEGER,

        experts TEXT,
                   
        confidence INTEGER,
        
        agreement INTEGER,
                   
        result TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()

    conn.close()

def save_decision(
    question,
    experts,
    risk,
    confidence,
    agreement,
    result
):

    conn = sqlite3.connect("data/council.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO decisions
        (
            question,
            experts,
            risk,
            confidence,
            agreement,
            result
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            question,
            experts,
            risk,
            confidence,
            agreement,
            result
        )
    )

    conn.commit()

    conn.close()


def get_history():

    conn = sqlite3.connect("data/council.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM decisions
        ORDER BY id DESC
        """
    )

    data = cursor.fetchall()

    conn.close()

    return data

def delete_decision(decision_id):

    conn = sqlite3.connect("data/council.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM decisions
        WHERE id = ?
        """,
        (decision_id,)
    )

    conn.commit()

    conn.close()
    print("delete_decision function loaded")


def get_total_decisions():

    conn = sqlite3.connect("data/council.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM decisions"
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total