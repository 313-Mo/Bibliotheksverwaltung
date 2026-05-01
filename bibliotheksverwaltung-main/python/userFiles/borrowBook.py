import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date


class BorrowBookClass():

    def __init__(self, root=None, db_path='../db/database.db'):
        self.root = root
        self.db_path = db_path

    #-----GUI FENSTER------
    def open_window(self, user_id):
        self.user_id = user_id

        self.window = tk.Toplevel(self.root)
        self.window.title("Buch ausleihen")
        self.center_window(self.window, 750, 520)

        frame = ttk.Frame(self.window, padding=15)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Buch auswählen (Doppelklick zum auswählen):",font=("Arial", 11, "bold")).pack(anchor="w", pady=(0, 10))

        #----Tabelle und Scrollbar-----
        table_frame = ttk.Frame(frame)
        table_frame.pack(fill="both", expand=True)

        columns = ("id", "title", "author", "year")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Titel")
        self.tree.heading("author", text="Autor")
        self.tree.heading("year", text="Jahr")

        self.tree.column("id", width=60, anchor="center")
        self.tree.column("title", width=300)
        self.tree.column("author", width=200)
        self.tree.column("year", width=80, anchor="center")

        #----Bücher laden------
        self.load_available_books()

        #-----Doppelklick------
        self.tree.bind("<Double-1>", self.borrow_selected_book)

        ttk.Button(self.window, text="Schließen", command=self.window.destroy).pack(pady=10)

    def load_available_books(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""SELECT id, title, author, year
                        FROM books
                        WHERE id NOT IN
                        (SELECT book_id FROM loans WHERE return_date IS NULL)
                        """)

        books = cursor.fetchall()
        conn.close()

        self.tree.delete(*self.tree.get_children())
        for book in books:
            self.tree.insert("", "end", values=book)

    def borrow_selected_book(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        book = self.tree.item(selected_item)["values"]
        book_id, title, author, year = book
        confirm = messagebox.askyesno(
            "Buch ausleihen",
            f"Möchtest du das Buch '{title}‘ wirklich ausleihen?"
        )

        if not confirm:
            return

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""INSERT INTO loans (user_id, book_id, loan_date)
                        VALUES (?, ?, ?)
                        """, (self.user_id, book_id, date.today()))

        conn.commit()
        conn.close()

        messagebox.showinfo("Erfolg", "Buch wurde ausgeliehen")

        self.load_available_books()

    def center_window(self, window, width, height):
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 2)

        window.geometry(f"{width}x{height}+{x}+{y}")

