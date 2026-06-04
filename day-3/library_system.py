# A simple library system that demonstrates the use of classes, inheritance, and the isinstance function in Python.
# The code defines a base class LibraryItem and two subclasses Book and EBook that inherit from LibraryItem. 
# Each class has its own attributes and a describe method that provides a string representation of the item.
# The code also includes examples of creating instances of the classes, calling their methods, and using isinstance to check the type of the instances.

class LibraryItem:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year
    
    def describe(self):
        return f"{self.title} by {self.author} ({self.year})"
    
class Book(LibraryItem):
    def __init__(self, title, author, year, pages):
        super().__init__(title, author, year)
        self.pages = pages
    
    def describe(self):
        return f"{super().describe()} - Pages: {self.pages}"
    
class EBook(LibraryItem):
    def __init__(self, title, author, year, file_size_mb):
        super().__init__(title, author, year)
        self.file_size = file_size_mb
    
    def describe(self):
        return f"{super().describe()} - File Size: {self.file_size} MB"
    
b1 = Book("The Great Gatsby", "F. Scott Fitzgerald", 1925, 218)
b2 = Book("1984", "George Orwell", 1949, 328)
eb1 = EBook("To Kill a Mockingbird", "Harper Lee", 1960, 2000)
eb2 = EBook("The Catcher in the Rye", "J.D. Salinger", 1951, 1800)
list_of_items = [b1, b2, eb1, eb2]
for item in list_of_items:
    print(item.describe())

print(f"Is b1 the instance of Book? {isinstance(b1, Book)}")  # True
print(f"Is b2 the instance of EBook? {isinstance(b2, EBook)}")  # False
print(f"Is eb1 the instance of Book? {isinstance(eb1, Book)}")  # False
print(f"Is eb2 the instance of EBook? {isinstance(eb2, EBook)}")  # True

# If we call isinstance(my_book, LibraryItem), it will return True because my_book is an instance of the Book class, which is a subclass of LibraryItem. 
# The isinstance function checks if the object is an instance of the specified class or any of its subclasses.
print(f"Is b1 the instance of LibraryItem? {isinstance(b1, LibraryItem)}")  # True
print(f"Is b2 the instance of LibraryItem? {isinstance(b2, LibraryItem)}")  # True
print(f"Is eb1 the instance of LibraryItem? {isinstance(eb1, LibraryItem)}")  # True
print(f"Is eb2 the instance of LibraryItem? {isinstance(eb2, LibraryItem)}")  # True

# Above 4 lines will return True because all the instances (b1, b2, eb1, eb2) are either instances of Book or EBook, which are subclasses of LibraryItem. Therefore, they are also considered instances of LibraryItem.
