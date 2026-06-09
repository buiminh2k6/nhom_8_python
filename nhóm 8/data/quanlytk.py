from page.login import LoginWindow
import tkinter as tk
from page.dangky import DangKy
from page.dashboard import Dashboard
class Quanlytk:
    def __init__(self, root):
        self.root = root
        self.score_data = {}
        self.show_login_window()
    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    def show_login_window(self):
        self.clear()
        self.current = LoginWindow(self.root, self)
    def show_dangky(self):
        self.clear()
        self.current = DangKy(self.root, self)
    def show_dashboard(self):
        self.clear()
        self.current = Dashboard(self.root, self)