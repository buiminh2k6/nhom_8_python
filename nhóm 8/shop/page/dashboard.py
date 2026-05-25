import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, filedialog
import shutil
from page.inventory import InventoryWindow
from page.category import CategoryWindow
from page.pos import POSWindow
from page.csv_handler import load_products, PROD_FILE

class Dashboard:
    def __init__(self, root, manager):
        self.root = root
        self.manager = manager
        self.root.title("Dashboard")
        self.root.geometry("700x450")
        
        frame = ctk.CTkFrame(root)
        frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(frame, text="HỆ THỐNG QUẢN LÝ CỬA HÀNG", font=("Arial", 22, "bold")).pack(pady=30)
        
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=10)
        
        ctk.CTkButton(btn_frame, text="Quản lý Kho hàng", width=200, height=40, font=("Arial", 14), command=self.open_inventory).grid(row=0, column=0, padx=15, pady=15)
        ctk.CTkButton(btn_frame, text="Quản lý Danh mục", width=200, height=40, font=("Arial", 14), command=self.open_category).grid(row=0, column=1, padx=15, pady=15)
        ctk.CTkButton(btn_frame, text="Bán hàng (POS)", width=200, height=40, font=("Arial", 14), command=self.open_pos).grid(row=1, column=0, padx=15, pady=15)
        ctk.CTkButton(btn_frame, text="Thống kê Bán chạy", width=200, height=40, font=("Arial", 14), command=self.show_top_selling).grid(row=1, column=1, padx=15, pady=15)
        ctk.CTkButton(btn_frame, text="Xuất CSV Báo cáo", width=200, height=40, font=("Arial", 14), command=self.export_csv).grid(row=2, column=0, columnspan=2, pady=15)
        ctk.CTkButton(btn_frame, text="Đăng xuất", width=200, height=40, font=("Arial", 14), fg_color="#C8504B", hover_color="#8c3632", command=self.manager.show_login_window).grid(row=3, column=0, columnspan=2, pady=10)
        
    def open_inventory(self):
        InventoryWindow(ctk.CTkToplevel(self.root))
        
    def open_category(self):
        CategoryWindow(ctk.CTkToplevel(self.root))
        
    def open_pos(self):
        POSWindow(ctk.CTkToplevel(self.root))
        
    def show_top_selling(self):
        products = load_products()
        sorted_prods = sorted(products, key=lambda x: int(x.get('SoldCount', 0)), reverse=True)
        msg = "Top 3 sản phẩm bán chạy:\n\n"
        for p in sorted_prods[:3]:
            msg += f"- {p['Name']} (Đã bán: {p.get('SoldCount', 0)})\n"
        messagebox.showinfo("Thống kê", msg)
        
    def export_csv(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")], title="Lưu báo cáo CSV")
        if filepath:
            shutil.copy(PROD_FILE, filepath)
            messagebox.showinfo("Thành công", f"Đã xuất dữ liệu ra {filepath}")