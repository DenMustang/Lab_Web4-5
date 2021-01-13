class Museum:
    def __init__(self, name=None, visitors=None, rooms=None):
        self.name = name
        self.visitors = visitors
        self.rooms = rooms

    def __str__(self):
        return f"Name:{self.name} Number of visitors per year:{self.visitors}" \
               f" Number of exhibition-rooms:{self.rooms}  "
