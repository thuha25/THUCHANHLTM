import server.database.connecter as connector

class ExamRoom:
    def __init__(self, id, description) -> None:
        self.id = id
        self.description = description
    
    @staticmethod
    def from_csv_row(row):
        return ExamRoom(*row)
    
    @staticmethod
    def get(id):
        cur = connector.get_cursor()
        cur.execute('SELECT * FROM exam_room WHERE id = ?', (id,))
        row = cur.fetchone()
        return ExamRoom.from_csv_row(row)
    
    @staticmethod
    def get_all():
        cur = connector.get_cursor()
        cur.execute('SELECT * FROM exam_room')
        rows = cur.fetchall()
        return [ExamRoom.from_csv_row(row) for row in rows]