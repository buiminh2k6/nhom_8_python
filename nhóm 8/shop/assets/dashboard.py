import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, filedialog
import shutil
import os
import webbrowser
import threading
import time
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
        ctk.CTkButton(btn_frame, text="Xuất CSV Báo cáo", width=200, height=40, font=("Arial", 14), command=self.export_csv).grid(row=2, column=0, padx=15, pady=15)
        ctk.CTkButton(btn_frame, text="Hướng dẫn sử dụng", width=200, height=40, font=("Arial", 14), command=self.open_manual).grid(row=2, column=1, padx=15, pady=15)
        ctk.CTkButton(btn_frame, text="Đăng xuất", width=200, height=40, font=("Arial", 14), fg_color="#C8504B", hover_color="#8c3632", command=self.manager.show_login_window).grid(row=3, column=0, columnspan=2, pady=10)
        
    def open_inventory(self):
        InventoryWindow(ctk.CTkToplevel(self.root))
        
    def open_category(self):
        CategoryWindow(ctk.CTkToplevel(self.root))
        
    def open_pos(self):
        POSWindow(ctk.CTkToplevel(self.root))

    def run_async_task(self, task_func, on_complete, loading_msg="Đang xử lý, vui lòng chờ..."):
        """Hàm chạy tác vụ ngầm tránh treo GUI với màn hình chờ"""
        loading_win = ctk.CTkToplevel(self.root)
        loading_win.title("Vui lòng chờ")
        loading_win.geometry("350x150")
        loading_win.transient(self.root)
        loading_win.grab_set() # Chặn thao tác với cửa sổ chính
        loading_win.protocol("WM_DELETE_WINDOW", lambda: None) # Ngăn đóng cửa sổ giữa chừng
        
        ctk.CTkLabel(loading_win, text=loading_msg, font=("Arial", 14)).pack(pady=20)
        progress = ctk.CTkProgressBar(loading_win, mode="indeterminate")
        progress.pack(pady=10, padx=20, fill="x")
        progress.start()
        
        task_result = {}
        
        def thread_target():
            try:
                time.sleep(3) # Giả lập tác vụ nặng tốn hơn 3 giây
                res = task_func()
                task_result['success'] = True
                task_result['data'] = res
            except Exception as e:
                task_result['success'] = False
                task_result['error'] = e
                
        # Khởi chạy luồng nền (Asynctask)
        thread = threading.Thread(target=thread_target, daemon=True)
        thread.start()
        
        def check_thread():
            if thread.is_alive():
                self.root.after(100, check_thread) # Hẹn giờ kiểm tra lại sau 100ms
            else:
                progress.stop()
                loading_win.destroy()
                if task_result.get('success'):
                    on_complete(task_result.get('data'))
                else:
                    messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {task_result.get('error')}")
                    
        # Bắt đầu vòng lặp kiểm tra
        check_thread()
        
    def show_top_selling(self):
        def task():
            products = load_products()
            return sorted(products, key=lambda x: int(x.get('SoldCount', 0)), reverse=True)
            
        def on_complete(sorted_prods):
            msg = "Top 3 sản phẩm bán chạy:\n\n"
            for p in sorted_prods[:3]:
                msg += f"- {p['Name']} (Đã bán: {p.get('SoldCount', 0)})\n"
            messagebox.showinfo("Thống kê", msg, parent=self.root)
            
        self.run_async_task(task, on_complete, "Đang tổng hợp dữ liệu thống kê...")
        
    def export_csv(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")], title="Lưu báo cáo CSV")
        if filepath:
            def task():
                shutil.copy(PROD_FILE, filepath)
                return filepath
                
            def on_complete(path):
                messagebox.showinfo("Thành công", f"Đã xuất dữ liệu ra {path}", parent=self.root)
                
            self.run_async_task(task, on_complete, "Đang xuất file CSV báo cáo...")
            
    def open_manual(self):
        # Giả định file PDF được đặt ở thư mục gốc của dự án (cùng cấp với main.py)
        pdf_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "HuongDanSuDung.pdf"))
        
        if os.path.exists(pdf_path):
            try:
                os.startfile(pdf_path)  # Lệnh mở file theo ứng dụng mặc định trên Windows
            except AttributeError:
                webbrowser.open_new(f"file://{pdf_path}")  # Fallback cho macOS/Linux
        else:
            messagebox.showerror("Lỗi", f"Không tìm thấy file Hướng dẫn sử dụng tại:\n{pdf_path}\n\nVui lòng kiểm tra lại!")