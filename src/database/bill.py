from database.connect import connect


def get_all_bill(user_id):
    bills = connect.cursor.execute("""
        SELECT * FROM bill 
        WHERE user_id = ?
    """, (user_id,)).fetchall()
    return {"code":1, "data":bills}
