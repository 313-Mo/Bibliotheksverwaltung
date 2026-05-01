import sqlite3
import tkinter as tk
from tkinter import ttk

class ShowAllLoanedBooks:
    def __init__(self, root=None, db_path='../db/database.db'):
        self.root = root
        self.db_path = db_path

    def open_window(self):
        self.window = tk.Toplevel(self.root)
        self.window.title("Alle momentan ausgeliehenen Bücher")
        self.center_window(self.window, 750, 520)

        frame = ttk.Frame(self.window, padding=15)
        frame.pack(fill="both", expand=True)

        filter_frame = ttk.Frame(frame)
        filter_frame.pack(fill="both", expand=True)

        ttk.Label(filter_frame, text="Suchen").pack(side="left")

        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(filter_frame, textvariable=self.search_var, width=40)
        search_entry.pack(side="left", padx=10)

        # ------Tabelle-------
        columns = ("id", "title", "author", "user", "loan_date")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        self.tree.pack(fill="both", expand=True)

        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Titel")
        self.tree.heading("author", text="Autor")
        self.tree.heading("user", text="Ausgeliehen von")
        self.tree.heading("loan_date", text="ausg. am")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("title", width=220)
        self.tree.column("author", width=150)
        self.tree.column("user", width=160)
        self.tree.column("loan_date", width=80, anchor="center")

        # ----Alle Bücher am Anfang laden-----
        self.books = self.get_all_loaned_books()
        self.fill_table(self.books)

        # ----Suchfunktion aktivieren-----
        self.search_var.trace_add("write", self.search_books)

        ttk.Button(self.window, text="Schließen", command=self.window.destroy).pack(pady=10)

    def center_window(self, window, width, height):
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 2)

        window.geometry(f"{width}x{height}+{x}+{y}")

    def fill_table(self, books):
        self.tree.delete(*self.tree.get_children())
        for book in books:
            self.tree.insert("", "end", values=book)

    def search_books(self, *args):
        term = self.search_var.get().lower()

        if term == "":
            self.fill_table(self.books)
            return

        filtered = [b for b in self.books if any(term in str(field).lower() for field in b)]
        self.fill_table(filtered)

    def get_all_loaned_books(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
                SELECT 
                    books.id,
                    books.title,
                    books.author,
                    users.name AS user,
                    loans.loan_date AS loan_date
                FROM books
                JOIN loans ON books.id = loans.book_id
                JOIN users ON users.id = loans.user_id
                WHERE loans.return_date IS NULL
            """)

        books = cursor.fetchall()
        conn.close()

        return books

