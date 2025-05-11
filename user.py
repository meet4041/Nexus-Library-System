# ------------ user.py ------------
class User:
    def __init__(self, user_id, name, role):
        self.user_id = user_id
        self.name = name
        self.role = role
        self.fines = 0
        self.borrowed_items = []

    def can_borrow(self):
        return len(self.borrowed_items) < self.max_borrow_limit()

    def max_borrow_limit(self):
        return 10

    def borrow_period(self):
        return 7

class Student(User):
    def max_borrow_limit(self):
        return 5

    def borrow_period(self):
        return 14  

class Faculty(User):
    def max_borrow_limit(self):
        return 8

    def borrow_period(self):
        return 20

class Researcher(User):
    def max_borrow_limit(self):
        return 10

    def borrow_period(self):
        return 30 

class Guest(User):
    def max_borrow_limit(self):
        return 2

    def borrow_period(self):
        return 7  # 1 week

class Professor(User):
    def __init__(self, user_id, name, role="professor"):
        super().__init__(user_id, name, role)
        self.faculty_role = Faculty(user_id, name, "faculty")
        self.researcher_role = Researcher(user_id, name, "researcher")
        self.roles = [self.faculty_role, self.researcher_role]

    def max_borrow_limit(self):
        return max(role.max_borrow_limit() for role in self.roles)

    def borrow_period(self):
        return max(role.borrow_period() for role in self.roles)
