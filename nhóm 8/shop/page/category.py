import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
from page.csv_handler import load_categories, save_categories

class CategoryWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý Danh mục")
        self.root.geometry("450x350")
        self.root.grab_set()
        self.categories = load_categories()
        
        form_frame = ctk.CTkFrame(root)
        form_frame.pack(fill=tk.X, padx=10, pady=10)
        ctk.CTkLabel(form_frame, text="Mã DM:", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.ent_id = ctk.CTkEntry(form_frame, width=200)
        self.ent_id.grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkLabel(form_frame, text="Tên DM:", font=("Arial", 12, "bold")).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.ent_name = ctk.CTkEntry(form_frame, width=200)
        self.ent_name.grid(row=1, column=1, padx=5, pady=5)
        
        btn_frame = ctk.CTkFrame(root, fg_color="transparent")
        btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text="Thêm Danh Mục", command=self.add_category).pack(side=tk.LEFT, padx=10)
        ctk.CTkButton(btn_frame, text="Quay lại", fg_color="gray", hover_color="darkgray", command=self.root.destroy).pack(side=tk.LEFT, padx=10)
        
        self.tree = ttk.Treeview(root, columns=("ID", "Name"), show='headings')
        self.tree.heading("ID", text="Mã DM")
        self.tree.heading("Name", text="Tên Danh Mục")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.refresh_table()

    def refresh_table(self):
        for row in self.tree.get_children(): self.tree.delete(row)
        for c in self.categories: self.tree.insert("", tk.END, values=(c['ID'], c['Name']))

    def add_category(self):
        cid, cname = self.ent_id.get().strip(), self.ent_name.get().strip()
        if cid and cname and not any(c['ID'] == cid for c in self.categories):
            self.categories.append({"ID": cid, "Name": cname})
            save_categories(self.categories)
            self.refresh_table()