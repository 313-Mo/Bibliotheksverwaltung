import sqlite3
from tkinter import ttk
from python.adminFiles.addBooks import AddBooksClass
from python.showBooks import ShowBooksClass
from python.adminFiles.showAllLoanedBooks import ShowAllLoanedBooks
from python.userFiles.borrowBook import BorrowBookClass
from python.userFiles.loaning import LoaningClass
from python.userFiles.returnBook import ReturnBookClass


class StudentLandingPage:
    def __init__(self, root):
        self.root = root
        self.add_books = AddBooksClass(root)
        self.show_books = ShowBooksClass(root)
        self.loaned_books = ShowAllLoanedBooks(root)
        self.loaning = LoaningClass(root)
        self.borrow = BorrowBookClass(root)
        self.return_book = ReturnBookClass(root)

    def open_window(self, user_id):
        self.clear_window()

        self.root.title("Bibliotheksverwaltung – Nutzer")
        self.center_window(750, 550)
        self.root.configure(bg="#dcdad4")

        # Styles
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Card.TFrame", background="#FFFFFF", relief="flat")
        style.configure("Header.TLabel", background="#FFFFFF", foreground="#1C1C1E", font=("SF Pro Display", 22, "bold"))
        style.configure("Subheader.TLabel", background="#FFFFFF", foreground="#3A3A3C", font=("SF Pro Text", 13))
        style.configure("Modern.TButton", font=("SF Pro Text", 14), padding=12,
                        background="#E5E5EA", foreground="#000000", relief="flat", borderwidth=0)
        style.map("Modern.TButton", background=[("active", "#D1D1D6")])

        # Zentrale Karte
        card = ttk.Frame(self.root, style="Card.TFrame", padding=30)
        card.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(card, text="Willkommen in der Bibliothek", style="Header.TLabel").pack(pady=(0, 10))
        ttk.Label(card, text="Was möchten Sie tun?", style="Subheader.TLabel").pack(pady=(0, 25))

        ttk.Button(card, text="Buch ausleihen", style="Modern.TButton",
                   command=lambda: self.borrow.open_window(user_id)).pack(fill="x", pady=8)

        ttk.Button(card, text="Alle Bücher ansehen", style="Modern.TButton",
                   command=self.show_books.open_window).pack(fill="x", pady=8)

        ttk.Button(card, text="Selbst ausgeliehene Bücher ansehen", style="Modern.TButton",
                   command=lambda: self.loaning.open_window(user_id)).pack(fill="x", pady=8)

        ttk.Button(card, text="Buch zurückgeben", style="Modern.TButton",
                   command=lambda: self.return_book.open_window(user_id)).pack(fill="x", pady=8)

        ttk.Button(card, text="Logout", style="Modern.TButton",
                   command=self.logout).pack(fill="x", pady=(30, 0))


    # Fenster zentrieren
    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 2)

        self.root.geometry(f"{width}x{height}+{x}+{y}")

    # Window leeren
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # Zurück zum Login
    def logout(self):
        from python.login import LoginScreen
        self.clear_window()
        LoginScreen(self.root)

