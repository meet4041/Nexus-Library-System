# ------------ library_item.py ------------
from state import Available, Reserved

class LibraryItem:
    def __init__(self, item_id, title, author):
        self.item_id = item_id
        self.title = title
        self.author = author
        self.borrow_date = None
        self.due_date = None
        self.state = Available()

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        self._state = new_state

    def checkout(self,user):
        if self.state is None:
            raise ValueError("Item state not initialized")
        self.state.checkout(self,user)

    def return_item(self):
        self.state.return_item(self)

    def reserve(self):
        self.state.reserve(self)

class EBook(LibraryItem):
    def __init__(self, item_id, title, author, format,genre):
        super().__init__(item_id, title, author)
        self.format = format
        self.genre = genre
        self.item_type = "EBook"

class PrintedBook(LibraryItem):
    def __init__(self, item_id, title, author, pages, genre):
        super().__init__(item_id, title, author)
        self.pages = pages
        self.genre = genre
        self.item_type = "Printed Book"

class ResearchPaper(LibraryItem):
    def __init__(self, item_id, title, author):
        super().__init__(item_id, title, author)
        self.genre = "research paper"
        self.state = Reserved()
        self.item_type = "Research Paper"

class Audiobook(LibraryItem):
    def __init__(self, item_id, title, author, duration):
        super().__init__(item_id, title, author)
        self.duration = duration  # Duration in minutes
        self.item_type = "Audio Book"

