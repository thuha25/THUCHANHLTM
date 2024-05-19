from server.data.examinator import Examinator

class RoomOrder:
    def __init__(self, id, examinator: Examinator, is_first: bool, room_id: str) -> None:
        self.id = id
        self.examinator = examinator
        self.is_first = is_first
        self.room_id = room_id
        
    def to_record(self):
        return (self.id, self.examinator.id, self.examinator.name, 'X' if self.is_first else '', 'X' if not self.is_first else '', self.room_id)