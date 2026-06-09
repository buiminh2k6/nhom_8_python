import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
import os
import shutil
from PIL import Image
from page.csv_handler import load_products, save_products, load_categories

ASSETS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets"))
os.makedirs(ASSETS_DIR, exist_ok=True)

class InventoryWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý Kho hàng")
        self.root.geometry("1000x700")
        self.root.grab_set()
        
        self.products = load_products()
        self.categories = [c['Name'] for c in load_categories()]
        
        form_frame = ctk.CTkFrame(root)
        form_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ctk.CTkLabel(form_frame, text="Mã ID:", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.ent_id = ctk.CTkEntry(form_frame, width=150)
        self.ent_id.grid(row=0, column=1, padx=5, pady=5)
        
        ctk.CTkLabel(form_frame, text="Tên SP:", font=("Arial", 12, "bold")).grid(row=0, column=2, padx=10, pady=10, sticky="w")
        self.ent_name = ctk.CTkEntry(form_frame, width=200)
        self.ent_name.grid(row=0, column=3, padx=5, pady=5)
        
        ctk.CTkLabel(form_frame, text="Loại:", font=("Arial", 12, "bold")).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.cb_category = ctk.CTkComboBox(form_frame, values=self.categories if self.categories else ["None"], width=150)
        self.cb_category.grid(row=1, column=1, padx=5, pady=5)
        
        ctk.CTkLabel(form_frame, text="Size:", font=("Arial", 12, "bold")).grid(row=1, column=2, padx=10, pady=10, sticky="w")
        self.ent_size = ctk.CTkEntry(form_frame, width=200)
        self.ent_size.grid(row=1, column=3, padx=5, pady=5)
        
        ctk.CTkLabel(form_frame, text="Giá bán:", font=("Arial", 12, "bold")).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.ent_price = ctk.CTkEntry(form_frame, width=150)
        self.ent_price.grid(row=2, column=1, padx=5, pady=5)
        
        ctk.CTkLabel(form_frame, text="Giá Sale:", font=("Arial", 12, "bold")).grid(row=2, column=2, padx=10, pady=10, sticky="w")
        self.ent_saleprice = ctk.CTkEntry(form_frame, width=200)
        self.ent_saleprice.grid(row=2, column=3, padx=5, pady=5)
        
        ctk.CTkLabel(form_frame, text="Số lượng:", font=("Arial", 12, "bold")).grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.ent_stock = ctk.CTkEntry(form_frame, width=150)
        self.ent_stock.grid(row=3, column=1, padx=5, pady=5)
        
        self.image_path = ""
        ctk.CTkButton(form_frame, text="Chọn ảnh", command=self.select_image, width=120).grid(row=3, column=2, padx=10, pady=10, sticky="w")
        
        self.lbl_image = ctk.CTkLabel(form_frame, text="Chưa có ảnh", width=120, height=120, fg_color="gray")
        self.lbl_image.grid(row=0, column=4, rowspan=4, padx=20, pady=10)
        
        btn_frame = ctk.CTkFrame(root, fg_color="transparent")
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        ctk.CTkButton(btn_frame, text="Thêm SP", width=100, command=self.add_product).pack(side=tk.LEFT, padx=10)
        ctk.CTkButton(btn_frame, text="Cập nhật", width=100, command=self.update_product).pack(side=tk.LEFT, padx=10)
        ctk.CTkButton(btn_frame, text="Xóa", width=100, fg_color="#C8504B", hover_color="#8c3632", command=self.delete_product).pack(side=tk.LEFT, padx=10)
        ctk.CTkButton(btn_frame, text="Quay lại", width=100, fg_color="gray", hover_color="darkgray", command=self.root.destroy).pack(side=tk.RIGHT, padx=10)
        
        search_frame = ctk.CTkFrame(root, fg_color="transparent")
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        ctk.CTkLabel(search_frame, text="Tìm kiếm (Tên):", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
        self.ent_search = ctk.CTkEntry(search_frame, width=200)
        self.ent_search.pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(search_frame, text="Tìm", width=80, command=self.search_product).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(search_frame, text="Làm mới", width=80, command=self.refresh_table).pack(side=tk.LEFT, padx=5)
        
        cols = ("ID", "Name", "Category", "Size", "Price", "SalePrice", "Stock", "SoldCount")
        self.tree = ttk.Treeview(root, columns=cols, show='headings')
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.tree.bind('<ButtonRelease-1>', self.on_select)
        
        self.refresh_table()

    def select_image(self):
        filepath = filedialog.askopenfilename(parent=self.root, title="Chọn ảnh sản phẩm", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if filepath:
            self.image_path = filepath
            self.show_image(filepath)

    def show_image(self, path):
        if path and os.path.exists(path):
            img = Image.open(path)
            ctk_img = ctk.CTkImage(light_image=img, size=(120, 120))
            self.lbl_image.configure(image=ctk_img, text="")
        else:
            self.lbl_image.configure(image=None, text="Chưa có ảnh")

    def refresh_table(self, data=None):
        for row in self.tree.get_children():
            self.tree.delete(row)
        items = data if data is not None else self.products
        for p in items:
            self.tree.insert("", tk.END, values=(p['ID'], p['Name'], p['Category'], p['Size'], p['Price'], p['SalePrice'], p['Stock'], p.get('SoldCount', 0)))

    def add_product(self):
        pid = self.ent_id.get().strip()
        if not pid:
            messagebox.showerror("Lỗi", "Mã ID không được để trống", parent=self.root)
            return
        if any(p['ID'] == pid for p in self.products):
            messagebox.showerror("Lỗi", "Mã ID đã tồn tại", parent=self.root)
            return
        
        saved_img_path = ""
        if self.image_path:
            ext = os.path.splitext(self.image_path)[1]
            saved_img_path = os.path.join(ASSETS_DIR, f"{pid}{ext}")
            shutil.copy(self.image_path, saved_img_path)
            
        new_prod = {
            "ID": pid, "Name": self.ent_name.get().strip(), "Category": self.cb_category.get().strip(),
            "Size": self.ent_size.get().strip(), "Price": self.ent_price.get().strip(),
            "SalePrice": self.ent_saleprice.get().strip(), "Stock": self.ent_stock.get().strip(),
            "SoldCount": "0", "ImagePath": saved_img_path
        }
        self.products.append(new_prod)
        save_products(self.products)
        self.refresh_table()
        messagebox.showinfo("Thành công", "Thêm sản phẩm thành công", parent=self.root)

    def update_product(self):
        pid = self.ent_id.get().strip()
        for p in self.products:
            if p['ID'] == pid:
                p.update({"Name": self.ent_name.get().strip(), "Category": self.cb_category.get().strip(),
                          "Size": self.ent_size.get().strip(), "Price": self.ent_price.get().strip(),
                          "SalePrice": self.ent_saleprice.get().strip(), "Stock": self.ent_stock.get().strip()})
                if self.image_path:
                    ext = os.path.splitext(self.image_path)[1]
                    saved_img_path = os.path.join(ASSETS_DIR, f"{pid}{ext}")
                    shutil.copy(self.image_path, saved_img_path)
                    p['ImagePath'] = saved_img_path
                break
        save_products(self.products)
        self.refresh_table()
        messagebox.showinfo("Thành công", "Cập nhật sản phẩm thành công", parent=self.root)

    def delete_product(self):
        selected = self.tree.selection()
        if selected:
            pid = self.tree.item(selected[0])['values'][0]
            self.products = [p for p in self.products if p['ID'] != str(pid)]
            save_products(self.products)
            self.refresh_table()
            messagebox.showinfo("Thành công", "Xóa sản phẩm thành công", parent=self.root)

    def search_product(self):
        query = self.ent_search.get().strip().lower()
        self.refresh_table([p for p in self.products if query in p['Name'].lower()])

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            vals = self.tree.item(selected[0])['values']
            for ent, val in zip([self.ent_id, self.ent_name, self.ent_size, self.ent_price, self.ent_saleprice, self.ent_stock], 
                                [vals[0], vals[1], vals[3], vals[4], vals[5], vals[6]]):
                ent.delete(0, tk.END)
                ent.insert(0, val)
            self.cb_category.set(vals[2])
        
        prod = next((p for p in self.products if p['ID'] == vals[0]), None)
        if prod and prod.get('ImagePath'):
            self.show_image(prod['ImagePath'])
        else:
            self.show_image("")