import server.database.connecter as connector

class Examinator:
    def __init__(self, id, name, date_of_birth, work_unit) -> None:
        self.id = id
        self.name = name
        self.date_of_birth = date_of_birth
        self.work_unit = work_unit
        
    @staticmethod
    def from_csv_row(row):
        return Examinator(*row)
    
    @staticmethod
    def get(id):
        cur = connector.get_cursor()
        cur.execute('SELECT * FROM examinator WHERE id = ?', (id,))
        row = cur.fetchone()
        return Examinator.from_csv_row(row)
    
    @staticmethod
    def get_all():
        cur = connector.get_cursor()
        cur.execute('SELECT * FROM examinator')
        rows = cur.fetchall()
        return [Examinator.from_csv_row(row) for row in rows]