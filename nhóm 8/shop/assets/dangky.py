import customtkinter as ctk
from tkinter import messagebox
import os

# Đường dẫn file dữ liệu
DATA_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "tk.csv"))

class DangKy:
    def __init__(self, root, manager):
        self.master = root
        self.manager = manager
        
        # Cấu hình cửa sổ
        self.master.title("Đăng ký")
        self.master.geometry("400x320")

        # Khởi tạo giao diện
        self.setup_ui()

    def setup_ui(self):
        """Hàm chuyên trách dựng giao diện"""
        # Main Frame
        self.frame = ctk.CTkFrame(self.master, width=320, height=260)
        self.frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)

        # Widgets nhập liệu
        ctk.CTkLabel(self.frame, text="Tên đăng nhập:", font=("Arial", 12, "bold")).pack(pady=(10, 2))
        self.entry_username = ctk.CTkEntry(self.frame, width=220)
        self.entry_username.pack(pady=2)

        ctk.CTkLabel(self.frame, text="Mật khẩu:", font=("Arial", 12, "bold")).pack(pady=(10, 2))
        self.entry_password = ctk.CTkEntry(self.frame, show="*", width=220)
        self.entry_password.pack(pady=2)
        
        ctk.CTkLabel(self.frame, text="Xác nhận mật khẩu:", font=("Arial", 12, "bold")).pack(pady=(10, 2))
        self.entry_confirm_password = ctk.CTkEntry(self.frame, show="*", width=220)
        self.entry_confirm_password.pack(pady=2)

        # Cụm nút bấm
        self.setup_buttons()

    def setup_buttons(self):
        """Tách cụm nút bấm ra để dễ điều chỉnh vị trí"""
        button_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        button_frame.pack(pady=15)
        
        self.button_dangky = ctk.CTkButton(
            button_frame, text="Đăng ký", width=100, 
            command=self.dangky
        )
        self.button_dangky.pack(side=ctk.LEFT, padx=10)

        self.button_back = ctk.CTkButton(
            button_frame, text="Quay lại", width=100, 
            fg_color="gray", hover_color="darkgray", 
            command=self.manager.show_login_window
        )
        self.button_back.pack(side=ctk.RIGHT, padx=10)

    def dangky(self):
        """Hàm xử lý logic đăng ký"""
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        confirm_password = self.entry_confirm_password.get().strip()

        # Kiểm tra rỗng
        if not username or not password or not confirm_password:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin.")
            return
            
        # Kiểm tra mật khẩu khớp nhau
        if password != confirm_password:
            messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp.")
            return

        # Xử lý lưu file
        try:
            os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
            with open(DATA_FILE, "a", encoding="utf-8") as file:
                file.write(f"{username},{password}\n")
            
            messagebox.showinfo("Đăng ký thành công", "Tài khoản đã được tạo.")
            self.manager.show_login_window()
        except Exception as e:
            messagebox.showerror("Lỗi hệ thống", f"Không thể lưu dữ liệu: {e}")