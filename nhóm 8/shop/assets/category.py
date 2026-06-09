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
        ctk.CTkButton(btn_frame, text="Thêm", width=80, command=self.add_category).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(btn_frame, text="Sửa", width=80, command=self.update_category).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(btn_frame, text="Xóa", width=80, fg_color="#C8504B", hover_color="#8c3632", command=self.delete_category).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(btn_frame, text="Quay lại", width=80, fg_color="gray", hover_color="darkgray", command=self.root.destroy).pack(side=tk.LEFT, padx=5)
        
        self.tree = ttk.Treeview(root, columns=("ID", "Name"), show='headings')
        self.tree.heading("ID", text="Mã DM")
        self.tree.heading("Name", text="Tên Danh Mục")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.tree.bind('<ButtonRelease-1>', self.on_select)
        
        self.refresh_table()

    def refresh_table(self):
        for row in self.tree.get_children(): self.tree.delete(row)
        for c in self.categories: self.tree.insert("", tk.END, values=(c['ID'], c['Name']))

    def add_category(self):
        cid, cname = self.ent_id.get().strip(), self.ent_name.get().strip()
        if not cid or not cname:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ Mã và Tên DM.", parent=self.root)
            return
        if any(c['ID'] == cid for c in self.categories):
            messagebox.showerror("Lỗi", "Mã danh mục đã tồn tại.", parent=self.root)
            return
            
        self.categories.append({"ID": cid, "Name": cname})
        save_categories(self.categories)
        self.refresh_table()
        messagebox.showinfo("Thành công", "Đã thêm danh mục mới.", parent=self.root)

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            vals = self.tree.item(selected[0])['values']
            self.ent_id.delete(0, tk.END)
            self.ent_id.insert(0, vals[0])
            self.ent_name.delete(0, tk.END)
            self.ent_name.insert(0, vals[1])

    def update_category(self):
        cid, cname = self.ent_id.get().strip(), self.ent_name.get().strip()
        for c in self.categories:
            if c['ID'] == str(cid):
                c['Name'] = cname
                save_categories(self.categories)
                self.refresh_table()
                messagebox.showinfo("Thành công", "Đã cập nhật danh mục.", parent=self.root)
                return
        messagebox.showerror("Lỗi", "Không tìm thấy mã danh mục để sửa.", parent=self.root)

    def delete_category(self):
        selected = self.tree.selection()
        if selected:
            cid = self.tree.item(selected[0])['values'][0]
            self.categories = [c for c in self.categories if c['ID'] != str(cid)]
            save_categories(self.categories)
            self.refresh_table()
            messagebox.showinfo("Thành công", "Đã xóa danh mục.", parent=self.root)