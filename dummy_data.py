# ------------ dummy_data.py ------------
from singleton_db import Database
from factory import UserFactory, LibraryItemFactory

def generate_dummy_data():
    db = Database()
    
    # Create dummy users
    users = [
        {"name": "John Doe", "role": "student", "id": "s101"},
        {"name": "Jane Smith", "role": "faculty", "id": "f201"},
        {"name": "Bob Wilson", "role": "researcher", "id": "r301"},
        {"name": "Guest User", "role": "guest", "id": "g401"},
        {"name": "Alice Brown", "role": "professor", "id": "p501"}
    ]
    
    for user in users:
        new_user = UserFactory.create_user(
            role=user["role"],
            user_id=user["id"],
            name=user["name"]
        )
        db.add_user(new_user)
    
    # Create dummy items
    items = [
        {"type": "ebook","item_id": "001", "title": "Python Programming", "author": "Eric Matthes", "format": "PDF", "genre": "Software Engineering"},
        {"type": "printed","item_id": "002", "title": "Clean Code", "author": "Robert Martin", "pages": 464, "genre": "Software Engineering"},
        {"type": "researchpaper","item_id": "003", "title": "AI Ethics", "author": "AI Research Team"},
        {"type": "audiobook", "item_id": "004","title": "Sapiens", "author": "Yuval Harari", "duration": 90},
        {"type": "printed","item_id": "005", "title": "The Pragmatic Programmer", "author": "Andrew Hunt", "pages": 352, "genre": "Software Engineering"},
        {"type": "printed","item_id": "006", "title": "Thinking, Fast and Slow", "author": "Daniel Kahneman", "pages": 512, "genre": "Psychology"},
        {"type": "printed","item_id": "007", "title": "Sapiens: A Brief History of Humankind", "author": "Yuval Noah Harari", "pages": 498, "genre": "History"},
        {"type": "printed","item_id": "008", "title": "A Brief History of Time", "author": "Stephen Hawking", "pages": 256, "genre": "Science"},
        {"type": "printed","item_id": "009", "title": "To Kill a Mockingbird", "author": "Harper Lee", "pages": 336, "genre": "Literature"}
    ]
    
    for idx, item in enumerate(items, 1):
        try:
            new_item = LibraryItemFactory.create_item(
                item_type=item["type"],
                item_id=item["item_id"],
                title=item["title"],
                author=item["author"],
                **{k:v for k,v in item.items() if k not in ["type","item_id", "title", "author"]}
            )
            db.add_item(new_item)
        except Exception as e:
            print(f"Fatal error creating item: {str(e)}")
    
    print("Generated:")
    print(f"- {len(users)} users")
    print(f"- {len(items)} items")

if __name__ == "__main__":
    generate_dummy_data()