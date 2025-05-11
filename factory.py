# ------------ factory.py ------------
from user import Student, Faculty, Researcher, Guest, Professor
from library_item import EBook, PrintedBook, ResearchPaper, Audiobook


class UserFactory:
    @staticmethod
    def create_user(role, user_id, name):
        role = role.lower()
        if role == "student":
            return Student(user_id, name, role)
        elif role == "faculty":
            return Faculty(user_id, name, role)
        elif role == "researcher":
            return Researcher(user_id, name, role)
        elif role == "professor":
            return Professor(user_id, name, role)
        elif role == "guest":
            return Guest(user_id, name, role)
        else:
            raise ValueError(f"Invalid user role: {role}")


class LibraryItemFactory:
    @staticmethod
    def create_item(item_type, **kwargs):
        try:
            if item_type == "ebook":
                return EBook(**kwargs)
            elif item_type == "printed":
                return PrintedBook(**kwargs)
            elif item_type == "researchpaper":
                return ResearchPaper(**kwargs)
            elif item_type == "audiobook":
                return Audiobook(**kwargs)
            else:
                raise ValueError(f"Invalid item type: {item_type}")
        except TypeError as e:
            print(f"Missing parameters for {item_type}: {str(e)}")
            return None
        except Exception as e:
            print(f"Error creating {item_type}: {str(e)}")
            return None
