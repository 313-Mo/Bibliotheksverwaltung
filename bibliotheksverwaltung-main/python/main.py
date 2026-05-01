import tkinter as tk
from tkinter import ttk
from adminFiles.addBooks import AddBooksClass
from showBooks import ShowBooksClass

def center_window(win):
    win.update_idletasks()
    w = win.winfo_width()
    h = win.winfo_height()
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    x = (sw - w) // 2
    y = (sh - h) // 2
    win.geometry(f"{w}x{h}+{x}+{y}")

def open_stub(title, text):
    w = tk.Toplevel(root)
    ttk.Label(w, text=text, padding=12).pack()
    ttk.Button(w, text="Schließen", command=w.destroy).pack(pady=8)
    center_window(w)

root = tk.Tk()
add_books = AddBooksClass(root)
show_books = ShowBooksClass(root)
root.title("Bibliotheks-Startseite")

# >>> RESPONSIVE Änderung
root.resizable(True, True)
root.geometry("800x650")
# <<<

style = ttk.Style(root)
style.theme_use("clam")
style.configure("TButton", font=("Segoe UI", 11), padding=8)
style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"))

try:
    img = tk.PhotoImage(file="book.png")
except Exception as e:
    img = None
    print("Bild konnte nicht geladen werden:", e)

# --- OBERER BEREICH ---
top = ttk.Frame(root, padding=(20,10))

# >>> RESPONSIVE Änderung
top.pack(fill="both", expand=True)
# <<<

if img:
    lbl_img = ttk.Label(top, image=img)
    lbl_img.pack()
    root.book_img = img

ttk.Label(top, text="Willkommen in der Bibliothek", style="Header.TLabel").pack(pady=(8,0))

# --- BUTTONBEREICH ---
btn_frame = ttk.Frame(root, padding=20)

# >>> RESPONSIVE Änderung
btn_frame.pack(fill="both", expand=True)
# <<<

btn_add = ttk.Button(btn_frame, text="Buch hinzufügen",
                     command=add_books.open_window)
btn_all_books = ttk.Button(btn_frame, text="Alle Bücher ansehen",
                    command=show_books.open_window)
btn_borrow = ttk.Button(btn_frame, text="Buch ausleihen",
                        command=lambda: open_stub("Buch ausleihen", "Hier: Auswahl verfügbarer Bücher"))
btn_view = ttk.Button(btn_frame, text="Ausgeliehene Bücher",
                      command=lambda: open_stub("Ausgeliehene Bücher", "Hier: Liste ausgeliehener Bücher"))
btn_quit = ttk.Button(btn_frame, text="Beenden", command=root.destroy)

for b in (btn_add, btn_all_books, btn_borrow, btn_view, btn_quit):
    # >>> responsive: Buttons dehnen sich mit
    b.pack(fill="x", pady=6)
    # <<<

center_window(root)
root.mainloop()



