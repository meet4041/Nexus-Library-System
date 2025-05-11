# ------------ singleton_db.py ------------
from state import Available, CheckedOut, Reserved
from datetime import datetime

class Database:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            
            # Initialize all attributes here
            cls._instance.users = []
            cls._instance.items = []
            cls._instance.transactions = []
            cls._instance.command_history = []

        return cls._instance
    
    def log_transaction(self, action, user_id, item_id):
        transaction = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "item_id": item_id,
            "action": action
        }
        self.transactions.append(transaction)

    @property
    def total_users(self):
        return len(self.users)
    
    @property
    def total_items(self):
        return len(self.items)

    @property
    def available_items(self):
        return len([i for i in self.items if isinstance(i.state, Available)])

    @property
    def borrowed_items(self):
        return len([i for i in self.items if isinstance(i.state, CheckedOut)])

    @property
    def reserved_items(self):
        return len([i for i in self.items if isinstance(i.state, Reserved)])

    def add_user(self, user):
        if user not in self.users:
            self.users.append(user)

    def remove_user(self, user_id):
        user = self.find_user(user_id)
        if user and not user.borrowed_items:
            self.users.remove(user)
            return True
        return False

    def add_item(self, item):
        if item and item not in self.items:
            self.items.append(item)
        else:
            print("Error: Attempted to add None item or duplicate item")
            return

    def remove_item(self, item_id):
        item = self.find_item(item_id)
        if item:
            if not isinstance(item.state, Available):
                print(f"Error: Cannot remove Checkedout item '{item_id}'")
                return False
            self.items.remove(item)
            return True
        return False
    
    def find_user(self, user_id):
        return next((u for u in self.users if u.user_id == user_id), None)
        
    def find_item(self, item_id):
        return next((i for i in self.items if i and i.item_id == item_id), None)