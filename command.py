# ------------ command.py ------------
from datetime import datetime, date, timedelta
from state import Available, CheckedOut, Reserved
from factory import EBook as eb, PrintedBook as pb, Audiobook as ab

class Command:
    def execute(self):
        pass

    def undo(self):
        pass

class BorrowCommand(Command):
    def __init__(self, db, user_id, item_id):
        self.db = db
        self.user_id = user_id
        self.item_id = item_id
        self.previous_state = None  # Only initialize once

    def execute(self):
        user = self.db.find_user(self.user_id)
        item = self.db.find_item(self.item_id)

        if not item:
            print("Error: Item not found")
            return False
        
        if isinstance(item.state, Reserved) and user.role.lower() not in ["faculty", "researcher"]:
            print("Item is Reserved")
            return False
            
        if not isinstance(item.state, Available) and not isinstance(item.state, Reserved):
            print("Item not available")
            return False
        
        # Role-based borrowing restrictions
        if user.role.lower() == "guest" and isinstance(item, eb):
            pass
        elif user.role.lower() == "student" and isinstance(item, (pb, eb, ab)):
            pass  
        elif user.role.lower() == "faculty":
            pass  
        elif user.role.lower() == "researcher":
            pass 
        elif user.role.lower() == "professor":
            pass
        else:
            print(f"{user.role.capitalize()} is not allowed to borrow this item type.")
            return False
         
        if not user.can_borrow():
            print("You have reached borrowing limit")
            return False

        try:
            self.previous_state = item.state
            item.checkout(user)
            user.borrowed_items.append(item)
            self.db.command_history.append(self)
            item.borrow_date = date.today()
            item.due_date = item.borrow_date + timedelta(days=user.borrow_period())
            self.db.log_transaction("BORROW", self.user_id, self.item_id)
            return True
        except Exception as e:
            print(f"Error: {str(e)}")
            return False

    def undo(self):
        user = self.db.find_user(self.user_id)
        item = self.db.find_item(self.item_id)

        if not user or not item:
            print("Undo failed: User or item not found")
            return False

        if not user.can_borrow():
            print("Undo failed: User reached borrowing limit")
            return False

        if user and item and item in user.borrowed_items:
            current_state = item.state
            item.state = self.previous_state
            user.borrowed_items.remove(item)
            return True
        return False


class ReturnCommand(Command):
    def __init__(self, db, user_id, item_id,return_date=None):
        self.db = db
        self.user_id = user_id
        self.item_id = item_id
        self.return_date = return_date
        self.fine_amount = 0
        self.previous_state = None

    def execute(self):
        try:
            user = self.db.find_user(self.user_id)
            item = self.db.find_item(self.item_id)

            if not item:
                print("Error: Item not found")
                return False
            
            if item not in user.borrowed_items:
                print("Error: This item isn't borrowed by the user")
                return False
            
            allowed_period = user.borrow_period()
            due_date = item.due_date or (item.borrow_date + timedelta(days=allowed_period))
            overdue_days = (self.return_date - due_date).days
            
            if overdue_days > 0:
                self.fine_amount = overdue_days * 15
                user.fines += self.fine_amount
                print(f"Late fee: ₹{self.fine_amount} ({overdue_days} days overdue)")
            else:
                print("Book returned on time. No fine.")

            self.previous_state = item.state
            item.return_item()
            user.borrowed_items.remove(item)
            self.db.command_history.append(self)
            self.db.log_transaction("RETURN", self.user_id, self.item_id)
            return True

        except Exception as e:
            print(f"Return failed: {str(e)}")
            return False

    def undo(self):
        try:
            user = self.db.find_user(self.user_id)
            item = self.db.find_item(self.item_id)

            if not user or not item:
                print("Undo failed: User or item not found")
                return False

            if not user.can_borrow():
                print("Undo failed: User reached borrowing limit")
                return False
            
            current_state = item.state
            item.state = self.previous_state
            user.borrowed_items.append(item)
            return True

        except Exception as e:
            print(f"Undo failed: {str(e)}")
            return False
        
