import tkinter as tk
from PIL import Image, ImageTk
import requests, io, os

# ---------------- Backend Classes ----------------
class Book:
    def __init__(self, book_id, title, author, stock):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.stock = stock

    def is_available(self):
        return self.stock > 0

    def update_stock(self, amount):
        self.stock += amount

class Member:
    def __init__(self, member_id, member_name):
        self.member_id = member_id
        self.member_name = member_name
        self.borrowed_books = []

    def borrow(self, book):
        if book.is_available():
            self.borrowed_books.append(book)
            book.update_stock(-1)
            return f"{self.member_name} borrowed '{book.title}'."
        return f"'{book.title}' is currently unavailable."

    def return_book(self, book):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
            book.update_stock(1)
            return f"{self.member_name} returned '{book.title}'."
        return f"{self.member_name} did not borrow '{book.title}'."

class Library:
    def __init__(self):
        self.book_collection = [
            Book(1, "Harry Potter", "J.K. Rowling", 5),
            Book(2, "The Hobbit", "J.R.R. Tolkien", 3),
            Book(3, "1984", "George Orwell", 4),
            Book(4, "To Kill a Mockingbird", "Harper Lee", 2)
        ]
        self.member_list = []
        self.load_members()

    def generate_book_id(self):
        return max([b.book_id for b in self.book_collection], default=0) + 1

    def load_members(self):
        if os.path.exists("members.txt"):
            with open("members.txt", "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) >= 2:
                        self.member_list.append(Member(int(parts[0]), ",".join(parts[1:])))
        else:
            open("members.txt", "w").close()

    def save_member(self, member):
        with open("members.txt", "a", encoding="utf-8") as f:
            f.write(f"{member.member_id},{member.member_name}\n")

    def add_book(self, title, author, stock):
        new_id = self.generate_book_id()
        self.book_collection.append(Book(new_id, title, author, stock))
        return f"'{title}' added successfully with ID {new_id}!"

    def show_all_books(self):
        return [f"ID: {b.book_id}, {b.title}, {b.author}, Stock: {b.stock}" for b in self.book_collection]

    def search_book(self, keyword):
        return [f"ID: {b.book_id}, {b.title}, {b.author}, Stock: {b.stock}"
                for b in self.book_collection if keyword.lower() in b.title.lower()]

    def register_member(self, member):
        if any(m.member_id == member.member_id for m in self.member_list):
            return f"Member ID {member.member_id} already exists!"
        self.member_list.append(member)
        self.save_member(member)
        return f"Member '{member.member_name}' registered successfully!"

    def borrow_book(self, member_id, book_id):
        member = next((m for m in self.member_list if m.member_id == member_id), None)
        book = next((b for b in self.book_collection if b.book_id == book_id), None)
        if member and book:
            return member.borrow(book)
        return "Invalid Member ID or Book ID."

    def return_book(self, member_id, book_id):
        member = next((m for m in self.member_list if m.member_id == member_id), None)
        book = next((b for b in self.book_collection if b.book_id == book_id), None)
        if member and book:
            return member.return_book(book)
        return "Invalid Member ID or Book ID."


# ---------------- GUI ----------------
BG_IMAGE_URL = "https://images.unsplash.com/photo-1637055159652-2b8837731f00?ixlib=rb-4.1.0&w=1200"

class LibraryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Library")
        self.root.geometry("555x755")
        self.root.resizable(False, False)

        self.library = Library()

        resp = requests.get(BG_IMAGE_URL)
        img_data = resp.content
        self.bg_image = Image.open(io.BytesIO(img_data))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.canvas = tk.Canvas(root, width=555, height=755, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        self.canvas.create_text(275, 90, text="Library Managemnet System", font=("Segoe UI", 20, "bold"), fill="#3A103A")

        enter = self.canvas.create_text(275, 150, text="ENTER", font=("Segoe UI", 16, "bold"), fill="#3A103A")
        self.canvas.tag_bind(enter, "<Button-1>", lambda e: self.show_second_screen())

    def show_second_screen(self):
        self.canvas.destroy()

        menu_width = 140
        self.left_frame = tk.Frame(self.root, bg="#1e1e2e", width=menu_width, height=755)
        self.left_frame.place(x=0, y=0)

        self.right_frame = tk.Frame(self.root, bg="black", width=555 - menu_width, height=755)
        self.right_frame.place(x=menu_width, y=0)

        options = ["View Books", "Add Book", "Search Book", "Register Member", "Borrow Book", "Return Book", "Exit"]
        for i, opt in enumerate(options):
            if opt == "Exit":
                cmd = self.root.destroy
            else:
                cmd = lambda opt=opt: self.update_right(opt)

            tk.Button(self.left_frame, text=opt, bg="#2e2e3e", fg="white",
                      font=("Segoe UI", 9), command=cmd).place(x=10, y=40 + i*60, width=120, height=35)

        self.r_widgets = []

    def clear_right(self):
        for w in self.r_widgets:
            w.destroy()
        self.r_widgets = []

    def update_right(self, option):
        self.clear_right()
        y = 20

        def lbl(t):
            nonlocal y
            L = tk.Label(self.right_frame, text=t, bg="black", fg="white", font=("Segoe UI", 10))
            L.place(x=10, y=y)
            self.r_widgets.append(L)
            y += 25

        def ent():
            nonlocal y
            E = tk.Entry(self.right_frame, width=22, font=("Segoe UI", 10))
            E.place(x=10, y=y)
            self.r_widgets.append(E)
            y += 35
            return E

        def btn(t, c):
            nonlocal y
            B = tk.Button(self.right_frame, text=t, command=c, bg="#2e2e3e", fg="white", font=("Segoe UI", 10))
            B.place(x=10, y=y)
            self.r_widgets.append(B)
            y += 40

        def out(t):
            nonlocal y
            O = tk.Label(self.right_frame, text=t, bg="black", fg="white", font=("Segoe UI", 9), anchor="w", justify="left")
            O.place(x=10, y=y)
            self.r_widgets.append(O)
            y += 20

        if option == "View Books":
            for b in self.library.show_all_books():
                out(b)

        elif option == "Add Book":
            lbl("Title:"); t = ent()
            lbl("Author:"); a = ent()
            lbl("Quantity:"); s = ent()
            btn("Add", lambda: out(self.library.add_book(t.get(), a.get(), int(s.get()))))

        elif option == "Search Book":
            lbl("Book Title:"); k = ent()
            btn("Search", lambda: [out(r) for r in self.library.search_book(k.get())] or out("Not Found."))

        elif option == "Register Member":
            lbl("Member ID:"); i = ent()
            lbl("Name:"); n = ent()
            btn("Register", lambda: out(self.library.register_member(Member(int(i.get()), n.get()))))

        elif option == "Borrow Book":
            lbl("Member ID:"); i = ent()
            lbl("Book ID:"); b = ent()
            btn("Borrow", lambda: out(self.library.borrow_book(int(i.get()), int(b.get()))))

        elif option == "Return Book":
            lbl("Member ID:"); i = ent()
            lbl("Book ID:"); b = ent()
            btn("Return", lambda: out(self.library.return_book(int(i.get()), int(b.get()))))


root = tk.Tk()
LibraryGUI(root)
root.mainloop()
