import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
from page.csv_handler import load_products, save_products

class POSWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Bán hàng & Thanh toán (POS)")
        self.root.geometry("1100x700")
        self.root.grab_set()
        self.products = load_products()
        self.cart = []
        
        left_frame = ctk.CTkFrame(root, width=600)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        ctk.CTkLabel(left_frame, text="Sản phẩm có sẵn", font=("Arial", 16, "bold")).pack(pady=10)
        
        cols = ("ID", "Name", "Size", "Price", "Stock")
        self.tree_prod = ttk.Treeview(left_frame, columns=cols, show='headings')
        for col in cols:
            self.tree_prod.heading(col, text=col)
            self.tree_prod.column(col, width=100)
        self.tree_prod.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.tree_prod.bind('<Double-1>', self.add_to_cart)
        self.refresh_products()
        
        right_frame = ctk.CTkFrame(root, width=450)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        ctk.CTkLabel(right_frame, text="Giỏ hàng", font=("Arial", 16, "bold")).pack(pady=10)
        
        cart_cols = ("ID", "Name", "Qty", "Total")
        self.tree_cart = ttk.Treeview(right_frame, columns=cart_cols, show='headings')
        for col in cart_cols:
            self.tree_cart.heading(col, text=col)
            self.tree_cart.column(col, width=90)
        self.tree_cart.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.lbl_total = ctk.CTkLabel(right_frame, text="Tổng tiền: 0", font=("Arial", 20, "bold"), text_color="#1f538d")
        self.lbl_total.pack(pady=10)
        ctk.CTkButton(right_frame, text="Thanh toán", font=("Arial", 16, "bold"), fg_color="#2FA572", hover_color="#106A43", height=50, command=self.checkout).pack(fill=tk.X, padx=20, pady=15)
        ctk.CTkButton(right_frame, text="Quay lại", font=("Arial", 14, "bold"), fg_color="gray", hover_color="darkgray", height=40, command=self.root.destroy).pack(fill=tk.X, padx=20, pady=5)

    def refresh_products(self):
        for row in self.tree_prod.get_children(): self.tree_prod.delete(row)
        for p in self.products:
            if int(p.get('Stock', 0)) > 0:
                self.tree_prod.insert("", tk.END, values=(p['ID'], p['Name'], p['Size'], p['SalePrice'] or p['Price'], p['Stock']))

    def add_to_cart(self, event):
        selected = self.tree_prod.selection()
        if not selected: return
        vals = self.tree_prod.item(selected[0])['values']
        pid, pname, price, stock = str(vals[0]), vals[1], float(vals[3]), int(vals[4])
        
        for c in self.cart:
            if c['ID'] == pid:
                if c['Qty'] < stock:
                    c['Qty'] += 1; c['Total'] = c['Qty'] * price
                    self.update_cart_ui()
                else: messagebox.showwarning("Cảnh báo", "Không đủ số lượng")
                return
        self.cart.append({"ID": pid, "Name": pname, "Qty": 1, "Price": price, "Total": price})
        self.update_cart_ui()

    def update_cart_ui(self):
        for row in self.tree_cart.get_children(): self.tree_cart.delete(row)
        total = sum(c['Total'] for c in self.cart)
        for c in self.cart: self.tree_cart.insert("", tk.END, values=(c['ID'], c['Name'], c['Qty'], c['Total']))
        self.lbl_total.config(text=f"Tổng tiền: {total}")

    def checkout(self):
        if not self.cart: return messagebox.showinfo("Thông báo", "Giỏ hàng trống")
        for c in self.cart:
            for p in self.products:
                if p['ID'] == c['ID']:
                    p['Stock'] = str(int(p['Stock']) - c['Qty'])
                    p['SoldCount'] = str(int(p.get('SoldCount', 0)) + c['Qty'])
        save_products(self.products); self.cart.clear(); self.update_cart_ui(); self.refresh_products()
        messagebox.showinfo("Thành công", "Thanh toán hoàn tất!")