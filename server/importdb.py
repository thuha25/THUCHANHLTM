import server.database.connecter as connector
import csv

def import_examinators(csv_path):
    cur = connector.get_cursor()
    cur.execute('DROP TABLE IF EXISTS examinator')
    cur.execute('CREATE TABLE IF NOT EXISTS examinator(id TEXT PRIMARY KEY, name TEXT, date_of_birth TEXT, work_unit TEXT)')
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            try:
                cur.execute('INSERT INTO examinator VALUES(?, ?, ?, ?)', row)
            except Exception as e:
                print(e)
                
    cur.connection.commit()
                
                
def import_rooms(csv_path):
    cur = connector.get_cursor()
    cur.execute('DROP TABLE IF EXISTS exam_room')
    cur.execute('CREATE TABLE IF NOT EXISTS exam_room(id TEXT PRIMARY KEY, description TEXT)')
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            try:
                cur.execute('INSERT INTO exam_room VALUES(?, ?)', row)
            except Exception as e:
                print(e)
                
    cur.connection.commit()
    

if __name__ == '__main__':
    cur = connector.get_cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS examinator(id TEXT PRIMARY KEY, name TEXT, date_of_birth TEXT, work_unit TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS exam_room(id TEXT PRIMARY KEY, description TEXT)')
    
    with open('examinator.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            try:
                cur.execute('INSERT INTO examinator VALUES(?, ?, ?, ?)', row)
            except Exception as e:
                print(e)
            
    with open('room.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            try:
                cur.execute('INSERT INTO exam_room VALUES(?, ?)', row)
            except Exception as e:
                print(e)
                
    cur.connection.commit()