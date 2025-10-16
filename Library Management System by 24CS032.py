import os

# Book Class
class Book:
    def __init__(self, book_id, title, author, stock):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.stock = stock

    def show_info(self):
        print(f"📘 ID: {self.book_id}, Title: {self.title}, Author: {self.author}, Stock: {self.stock}")

    def is_available(self):
        return self.stock > 0

    def update_stock(self, amount):
        self.stock += amount


# Member Class
class Member:
    def __init__(self, member_id, member_name):
        self.member_id = member_id
        self.member_name = member_name
        self.borrowed_books = []

    def borrow(self, book):
        if book.is_available():
            self.borrowed_books.append(book)
            book.update_stock(-1)
            print(f"✅ {self.member_name} borrowed '{book.title}'.")
        else:
            print(f"❌ '{book.title}' is currently unavailable.")

    def return_book(self, book):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
            book.update_stock(1)
            print(f"🔁 {self.member_name} returned '{book.title}'.")
        else:
            print(f"⚠️ {self.member_name} did not borrow '{book.title}'.")


# Library Class
class Library:
    def __init__(self):
        self.book_collection = [
            Book(1, "Harry Potter and the Sorcerer's Stone", "J.K. Rowling", 5),
            Book(2, "The Hobbit", "J.R.R. Tolkien", 3),
            Book(3, "1984", "George Orwell", 4),
            Book(4, "To Kill a Mockingbird", "Harper Lee", 2)
        ]
        self.member_list = []
        self.load_members()

    # Generate unique book ID
    def generate_book_id(self):
        if not self.book_collection:
            return 1
        return max(book.book_id for book in self.book_collection) + 1

    # Load members from file
    def load_members(self):
        if os.path.exists("members.txt"):
            with open("members.txt", "r") as file:
                for line in file:
                    member_id, member_name = line.strip().split(",")
                    self.member_list.append(Member(int(member_id), member_name))
        else:
            open("members.txt", "w").close()

    # Save new member to file
    def save_member(self, member):
        with open("members.txt", "a") as file:
            file.write(f"{member.member_id},{member.member_name}\n")

    def add_book(self, title, author, stock):
        new_id = self.generate_book_id()
        self.book_collection.append(Book(new_id, title, author, stock))
        print(f"📚 '{title}' added successfully with ID {new_id}!")

    def show_all_books(self):
        if not self.book_collection:
            print("No books available in the library.")
        else:
            for book in self.book_collection:
                book.show_info()

    def search_book(self, keyword):
        return [book for book in self.book_collection if keyword.lower() in book.title.lower()]

    def register_member(self, member):
        if any(m.member_id == member.member_id for m in self.member_list):
            print("⚠️ Member ID already exists!")
        else:
            self.member_list.append(member)
            self.save_member(member)
            print(f"👤 Member '{member.member_name}' registered successfully and saved to file!")

    def borrow_book(self, member_id, book_id):
        member = next((m for m in self.member_list if m.member_id == member_id), None)
        book = next((b for b in self.book_collection if b.book_id == book_id), None)
        if member and book:
            member.borrow(book)
        else:
            print("❌ Invalid Member ID or Book ID.")

    def return_book(self, member_id, book_id):
        member = next((m for m in self.member_list if m.member_id == member_id), None)
        book = next((b for b in self.book_collection if b.book_id == book_id), None)
        if member and book:
            member.return_book(book)
        else:
            print("❌ Invalid Member ID or Book ID.")


# Main Program
def main():
    library = Library()

    while True:
        print("\n===== 📖 Library Management Menu =====")
        print("1. View All Books")
        print("2. Add Book")
        print("3. Search Book by Title")
        print("4. Register Member")
        print("5. Borrow Book")
        print("6. Return Book")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            library.show_all_books()

        elif choice == '2':
            try:
                title = input("Enter Book Title: ")
                author = input("Enter Author Name: ")
                stock = int(input("Enter Quantity: "))
                library.add_book(title, author, stock)
            except ValueError:
                print("⚠️ Invalid input! Quantity must be a number.")

        elif choice == '3':
            title = input("Enter Book Title to Search: ")
            results = library.search_book(title)
            if results:
                for book in results:
                    book.show_info()
            else:
                print("No matching books found.")

        elif choice == '4':
            try:
                member_id = int(input("Enter Member ID: "))
                name = input("Enter Member Name: ")
                library.register_member(Member(member_id, name))
            except ValueError:
                print("⚠️ Invalid Member ID! Please enter a numeric value.")

        elif choice == '5':
            try:
                member_id = int(input("Enter Member ID: "))
                book_id = int(input("Enter Book ID to Borrow: "))
                library.borrow_book(member_id, book_id)
            except ValueError:
                print("⚠️ Invalid input! Member ID and Book ID must be numbers.")

        elif choice == '6':
            try:
                member_id = int(input("Enter Member ID: "))
                book_id = int(input("Enter Book ID to Return: "))
                library.return_book(member_id, book_id)
            except ValueError:
                print("⚠️ Invalid input! Member ID and Book ID must be numbers.")

        elif choice == '7':
            print("👋 Exiting... Have a great day!")
            break

        else:
            print("❗ Invalid choice, please try again.")


main()
