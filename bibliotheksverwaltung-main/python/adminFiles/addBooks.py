import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import requests

class AddBooksClass:
    def __init__(self, root=None, db_path='../db/database.db'):
        self.root = root
        self.db_path = db_path

    #-------Methoden-------

    #-------Buch mit übergebenen infos hinzufügen
    def add_book(self, title, author, genre, year):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO books (title, author, genre, year)
            VALUES (?, ?, ?, ?)
            """, (title, author, genre, year))

        conn.commit()
        conn.close()


    #------Buch hinzufügen über Konsole------
    def input_book(self):
        print("Neuen Buchtitel eingeben:")
        title = input("Titel: ")
        author = input("Author: ")
        genre = input("Genre: ")
        year = input("Jahr: ")

        year = int(year) if year.isdigit() else None

        self.add_book(title, author, genre, year)
        print("\nBuch wurde hinzugefügt! ")


    #-------Buch hinzufügen über Konsole mit ISBN---------
    def input_books_isbn(self, isbn):
        isbnString = isbn.replace("-", "")
        if len(isbnString) == 10:
            cleanedISBN = isbn
        else:
            numString = str(isbnString)[3:-1]
            multiplikator = 10
            result = 0
            for zahl in numString:
                result += int(zahl) * multiplikator
                multiplikator -= 1
            result = result % 11
            if result == 0:
                result = 0
            else:
                result = 11 - result
            cleanedISBN = numString + str(result)

        url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{cleanedISBN}&format=json&jscmd=data"
        response = requests.get(url)

        if response.status_code != 200:
            print("Fehler: API konnte nicht erreicht werden.")
            return "API Fehler"

        data = response.json()
        key = f"ISBN:{cleanedISBN}"

        if key not in data:
            print("Es wurde kein Buch mit dieser ISBN gefunden!")
            return "ISBN nicht gefunden"

        book = data[key]

        title = book.get("title", "Unbekannt")
        if "authors" in book:
            author = ", ".join(a["name"] for a in book["authors"])
        else:
            author = "Unbekannt"

        # ----- Genre ----- vielleicht in Seitenanzahl ändern?
        if "subjects" in book and len(book["subjects"]) > 0:
            genre = book["subjects"][0]["name"]
        else:
            genre = "Unbekannt"

        # ----- Jahr aus publish_date extrahieren -----
        raw_year = book.get("publish_date", "")  # könnte z. B. "July 1997" sein
        digits = "".join(c for c in raw_year if c.isdigit())
        year = int(digits[:4]) if len(digits) >= 4 else None


        # In DB speichern
        self.add_book(title, author, genre, year)
        print("\nBuch wurde hinzugefügt!")
        return None

    #-----Alle Bücher in der Konsole anzeigen-------
    def show_books(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()

        conn.close()

        if not books:
            print("Keine Bücher in der Datenbank!")
            return

        print("Folgende Bücher sind in der Bibliothek enthalten!")
        for book in books:
            print(book)

    #------GUI Fenster------

    def open_window(self):
        self.window = tk.Toplevel(self.root)
        self.window.title("Buch hinzufügen")
        self.window.resizable(False, False)

        self.center_window(self.window, 450, 380)

        frame = ttk.Frame(self.window, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Neues Buch eintragen",
                  font=("Segoe UI", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 15))
        ttk.Button(frame, text="Buch per ISBN hinzufügen",
                   command=self.open_isbn_window).grid(row=1, column=0, columnspan=2, pady=10)

        #Eingabefelder
        ttk.Label(frame, text="Titel:").grid(row=2, column=0, sticky="w")
        self.entry_title = ttk.Entry(frame, width=40)
        self.entry_title.grid(row=2, column=1)

        ttk.Label(frame, text="Autor:").grid(row=3, column=0, sticky="w")
        self.entry_author = ttk.Entry(frame, width=40)
        self.entry_author.grid(row=3, column=1)

        ttk.Label(frame, text="Genre:").grid(row=4, column=0, sticky="w")
        self.entry_genre = ttk.Entry(frame, width=40)
        self.entry_genre.grid(row=4, column=1)

        ttk.Label(frame, text="Jahr:").grid(row=5, column=0, sticky="w")
        self.entry_year = ttk.Entry(frame, width=40)
        self.entry_year.grid(row=5, column=1)

        ttk.Button(frame, text="Speichern", command=self.save_manual).grid(
            row=6, column=0, columnspan=2, pady=20
        )

    def center_window(self, window, width, height):
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 2)

        window.geometry(f"{width}x{height}+{x}+{y}")

    def save_manual(self):
        title = self.entry_title.get()
        author = self.entry_author.get()
        genre = self.entry_genre.get()
        year = self.entry_year.get()

        if not title or not author:
            print("Fehler, gebe mindestens den Titel und den Autor ein!")
            return

        year = int(year) if year.isdigit() else None

        self.add_book(title, author, genre, year)
        messagebox.showinfo("Erfolg", "Das Buch wurde erfolgreich hinzugefügt!")
        self.window.destroy()

    def open_isbn_window(self):
        self.isbn_window = tk.Toplevel(self.root)
        self.isbn_window.title("Buch per ISBN hinzufügen")
        self.isbn_window.resizable(False, False)

        self.center_window(self.isbn_window, 350, 180)

        frame = ttk.Frame(self.isbn_window, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="ISBN eingeben:", font=("Segoe UI", 12)).pack()
        self.entry_isbn = ttk.Entry(frame, width=30)
        self.entry_isbn.pack(pady=5)

        ttk.Button(frame, text="Hinzufügen", command=self.save_isbn).pack(pady=10)

    def save_isbn(self):
        isbn = self.entry_isbn.get().strip()
        result = self.input_books_isbn(isbn)

        if result is None:
            messagebox.showinfo("Erfolg", "Buch wurde erfolgreich hinzugefügt!")
            self.isbn_window.destroy()
        else:
            messagebox.showerror("Fehler", result)

if __name__ == "__main__":
    manager = AddBooksClass()
    manager.show_books()

