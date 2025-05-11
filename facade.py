# ------------ facade.py ------------
from command import BorrowCommand, ReturnCommand
from state import Available, CheckedOut, Reserved

class LibraryFacade:
    def __init__(self, db):
        self.db = db
        self._search_strategy = None
        self._notification_service = None

    def borrow_item(self, user_id, item_id):
        command = BorrowCommand(self.db, user_id, item_id)
        if command.execute():
            self._notify_borrow_success(user_id, item_id)
            return True
        return False

    def return_item(self, user_id, item_id,return_date=None):
        command = ReturnCommand(self.db, user_id, item_id, return_date)
        if command.execute():
            self.db.command_history.append(command)
            self._notify_return_success(user_id, item_id)
            return True
        return False
    
    def set_search_strategy(self, strategy):
        self.current_strategy = strategy  # Default stratergy

    def search_items(self, query, strategy=None):
        search_strategy = strategy or self.current_strategy
        return search_strategy.search(self.db.items, query)


    def get_user_borrowed_items(self, user_id):
        user = self.db.find_user(user_id)
        return user.borrowed_items if user else []

    def undo_last_action(self):
        if self.db.command_history:
            last_command = self.db.command_history.pop()
            last_command.undo()
            print("Last action undone!")
            return True
        return False

    def reserve_item(self, user_id, item_id):
        item = self.db.find_item(item_id)
        if item and isinstance(item.state, Available):
            item.reserve()
            self._notify_reservation(user_id, item_id)
            return True
        return False

    def _notify_borrow_success(self, user_id, item_id):
        if self._notification_service:
            user = self.db.find_user(user_id)
            item = self.db.find_item(item_id)
            self._notification_service.notify(
                user,
                f"Item {item.title} borrowed successfully. Due date: {item.due_date}"
            )

    def _notify_return_success(self, user_id, item_id):
        if self._notification_service:
            user = self.db.find_user(user_id)
            item = self.db.find_item(item_id)
            self._notification_service.notify(
                user,
                f"Item {item.title} returned successfully"
            )

    def _notify_reservation(self, user_id, item_id):
        if self._notification_service:
            user = self.db.find_user(user_id)
            item = self.db.find_item(item_id)
            self._notification_service.notify(
                user,
                f"Item {item.title} reserved successfully"
            )