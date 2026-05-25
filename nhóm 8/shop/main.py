import customtkinter as ctk
from tkinter import ttk
from quanlytk import Quanlytk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()

style = ttk.Style(root)
style.theme_use("default")
style.configure("Treeview", background="#2b2b2b", foreground="white", rowheight=25, fieldbackground="#2b2b2b", borderwidth=0)
style.map('Treeview', background=[('selected', '#1f538d')])
style.configure("Treeview.Heading", background="#565b5e", foreground="white", relief="flat", font=("Arial", 10, "bold"))
style.map("Treeview.Heading", background=[('active', '#1f538d')])

app = Quanlytk(root)
root.mainloop()