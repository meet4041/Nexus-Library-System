# ------------ state.py ------------

class State:
    def checkout(self, item, user):
        pass

    def return_item(self, item):
        pass

    def reserve(self, item):
        pass

class Available(State):
    def checkout(self, item, user):
        print(f"{item.title} checked out by {user.name}")
        item.state = CheckedOut()

    def reserve(self, item):
        print(f"{item.title} reserved")
        item.state = Reserved()

class CheckedOut(State):
    def return_item(self, item):
        print(f"{item.title} returned")
        item.state = Available()

class Reserved(State):
    def checkout(self, item, user):
        if user.role.lower() in ["faculty", "researcher"]:
            print(f"Reserved item '{item.title}' checked out by {user.role.capitalize()} {user.name}")
            item.state = CheckedOut()
        else:
            print("Reserved item")