import customtkinter as ctk
from tkinter import ttk
from quanlytk import Quanlytk

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()

style = ttk.Style(root)
style.theme_use("default")
style.configure("Treeview", background="#ffffff", foreground="black", rowheight=25, fieldbackground="#ffffff", borderwidth=0)
style.map('Treeview', background=[('selected', '#1f538d')], foreground=[('selected', 'white')])
style.configure("Treeview.Heading", background="#e0e0e0", foreground="black", relief="flat", font=("Arial", 10, "bold"))
style.map("Treeview.Heading", background=[('active', '#c0c0c0')])

app = Quanlytk(root)
root.mainloop()