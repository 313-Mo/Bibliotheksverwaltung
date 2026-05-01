import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import re

from adminFiles.adminLandingPage import AdminLandingPage
from userFiles.studentLandingPage import StudentLandingPage

class LoginScreen:
    def __init__(self, root=None, db_path='../db/database.db'):
        self.root = root
        self.root.title("Login")
        self.db_path = db_path

        # Seiten vorbereiten


        # Fenster zentrieren
        self.center_window(400, 350)

        # --- Hintergrundfarbe wie Admin-Seite ---
        self.root.configure(bg="#dcdad4")

        # --- Styles setzen (gleich wie AdminLandingPage) ---
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Card.TFrame", background="#FFFFFF", relief="flat")
        style.configure("Header.TLabel", background="#FFFFFF", foreground="#1C1C1E",
                        font=("SF Pro Display", 22, "bold"))
        style.configure("Subheader.TLabel", background="#FFFFFF", foreground="#3A3A3C",
                        font=("SF Pro Text", 13))

        style.configure("Modern.TButton",
            font=("SF Pro Text", 14),
            padding=10,
            background="#E5E5EA",
            foreground="#000000",
            relief="flat",
            borderwidth=0
        )
        style.map("Modern.TButton", background=[("active", "#D1D1D6")])

        # --- Karte (weißer Container) ---
        card = ttk.Frame(self.root, style="Card.TFrame", padding=30)
        card.place(relx=0.5, rely=0.5, anchor="center")

        # Texte
        ttk.Label(card, text="Willkommen", style="Header.TLabel").pack(pady=(0, 10))
        ttk.Label(card, text="Bitte anmelden", style="Subheader.TLabel").pack(pady=(0, 20))

        # Eingabefeld E-Mail
        ttk.Label(card, text="E-Mail:", background="#FFFFFF", foreground="#1C1C1E",
                  font=("SF Pro Text", 12)).pack(anchor="w")
        self.email_entry = ttk.Entry(card, width=35)
        self.email_entry.pack(pady=(0, 10))

        # Eingabefeld Passwort
        ttk.Label(card, text="Passwort:", background="#FFFFFF", foreground="#1C1C1E",
                  font=("SF Pro Text", 12)).pack(anchor="w")
        self.password_entry = ttk.Entry(card, width=35, show="*")
        self.password_entry.pack(pady=(0, 20))

        # Login-Button
        ttk.Button(card, text="Login", style="Modern.TButton",
                   command=self.login).pack(fill="x")

    # -----------------------------
    def center_window(self, width, height):
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = int((screen_w - width) / 2)
        y = int((screen_h - height) / 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    # -----------------------------
    def extract_name(self, email):
        local = email.split("@")[0]
        first, last = local.split(".")
        return first.capitalize() + " " + last.capitalize()

    # -----------------------------
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # -----------------------------
    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not email or not password:
            messagebox.showerror("Fehler", "Bitte E-Mail und Passwort eingeben!")
            return

        # Admin Login
        if email == "admin" and password == "admin":
            self.clear_window()
            AdminLandingPage(self.root).open_window()
            return

        # Studenten-E-mail prüfen
        student_pattern = r"^[a-zA-Z]+\.[a-zA-Z]+@stud\.th-luebeck\.de$"
        if not re.match(student_pattern, email):
            messagebox.showerror("Fehler", "Ungültige Studenten-E-Mail!")
            return

        # DB lookup
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
        result = cursor.fetchone()

        # Student existiert noch nicht, also neu speichern
        if result is None:
            name = self.extract_name(email)
            cursor.execute("""
                INSERT INTO users (name, email, password)
                VALUES (?, ?, ?)
            """, (name, email, password))
            conn.commit()
            cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
            user_id = cursor.fetchone()[0]
            conn.close()

            self.clear_window()
            StudentLandingPage(self.root).open_window(user_id)
            return

        # Passwort prüfen
        stored_pw = result[0]
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        user_id = cursor.fetchone()[0]
        conn.close()

        if stored_pw == password:
            self.clear_window()
            StudentLandingPage(self.root).open_window(user_id)
        else:
            messagebox.showerror("Fehler", "Falsches Passwort!")

# Start
if __name__ == "__main__":
    root = tk.Tk()
    LoginScreen(root)
    root.mainloop()

    