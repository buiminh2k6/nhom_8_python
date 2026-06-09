import customtkinter as ctk
from tkinter import messagebox
import os

DATA_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "tk.csv"))

class LoginWindow:
    def __init__(self, root, manager):
        self.master = root
        self.manager = manager

        # Cấu hình cửa sổ
        self.master.title("Đăng nhập")
        self.master.geometry("400x250")
        
        # Khởi tạo giao diện
        self.setup_ui()

    def setup_ui(self):
        """Hàm chuyên trách dựng giao diện"""
        # Main Frame
        self.frame = ctk.CTkFrame(self.master, width=320, height=180)
        self.frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)

        # Widgets nhập liệu
        ctk.CTkLabel(self.frame, text="Username:", font=("Arial", 12, "bold")).pack(pady=(10, 2))
        self.entry_username = ctk.CTkEntry(self.frame, width=220)
        self.entry_username.pack(pady=2)

        ctk.CTkLabel(self.frame, text="Password:", font=("Arial", 12, "bold")).pack(pady=(10, 2))
        self.entry_password = ctk.CTkEntry(self.frame, show="*", width=220)
        self.entry_password.pack(pady=2)

        # Cụm nút bấm
        self.setup_buttons()

    def setup_buttons(self):
        """Tách cụm nút bấm ra để dễ điều chỉnh vị trí"""
        button_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        button_frame.pack(pady=15)

        btn_login = ctk.CTkButton(button_frame, text="Đăng nhập", width=100, command=self.login)
        btn_login.pack(side=ctk.LEFT, padx=10)

        btn_dangky = ctk.CTkButton(button_frame, text="Đăng ký", width=100, command=self.dangky)
        btn_dangky.pack(side=ctk.RIGHT, padx=10)

    def login(self):
        """Hàm xử lý logic đăng nhập"""
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if not username or not password:
            messagebox.showerror("Lỗi", "Vui lòng nhập tên đăng nhập và mật khẩu.")
            return

        if not os.path.exists(DATA_FILE):
            messagebox.showerror("Lỗi", "Chưa có tài khoản. Vui lòng đăng ký trước.")
            return

        with open(DATA_FILE, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) >= 2:
                    stored_username = parts[0]
                    stored_password = parts[1]
                    if username == stored_username and password == stored_password:
                        messagebox.showinfo("Đăng nhập thành công", f"Chào mừng, {username}!")
                        self.manager.show_dashboard()
                        return

        messagebox.showerror("Đăng nhập thất bại", "Tên đăng nhập hoặc mật khẩu không đúng.")

    def dangky(self):
        """Chuyển hướng sang màn hình đăng ký"""
        self.manager.show_dangky()