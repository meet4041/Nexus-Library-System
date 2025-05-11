# ------------ strategy.py ------------
from abc import ABC, abstractmethod

class SearchStrategy(ABC):
    @abstractmethod
    def search(self, items, query):
        pass

class KeywordSearchStrategy(SearchStrategy):
    def search(self, items, query):
        query = query.strip().lower()
        results = []
        seen_items = set()
        
        for item in items:
            try:
                # Check all relevant fields including author
                matches = any([
                    query in item.title.lower(),
                    query in item.author.lower(), 
                    (hasattr(item, 'genre') and query in item.genre.lower())
                ])
                
                if matches and item.item_id not in seen_items:
                    results.append(item)
                    seen_items.add(item.item_id)
            except AttributeError as e:
                print(f"Skipping invalid item: {str(e)}")
                continue
        print(f"Found {len(results)} genre matches")
        return results

class AuthorSearchStrategy(SearchStrategy):
    """Search by author name (case-insensitive partial match)"""
    def search(self, items, query):
        query = query.strip().lower()
        results = []
        for item in items:
            try:
                if query in item.author.lower():
                    results.append(item)
            except AttributeError:
                continue
        print(f"Found {len(results)} genre matches")
        return results

class GenreSearchStrategy(SearchStrategy):
    """Search by genre (case-insensitive partial match)"""
    def search(self, items, query):
        query = query.strip().lower()
        results = []
        for item in items:
            try:
                if hasattr(item, 'genre') and query in item.genre.lower():
                    results.append(item)
            except AttributeError:
                continue
        print(f"Found {len(results)} genre matches")
        return results