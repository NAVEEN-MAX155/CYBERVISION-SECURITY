import customtkinter as ctk
from tkinter import messagebox
from modules.register_face import register_face


class RegisterWindow(ctk.CTkToplevel):

    def __init__(self):
        super().__init__()

        self.title("Register Face")
        self.geometry("450x250")
        self.resizable(False, False)
        self.lift()
        self.attributes("-topmost", True)
        self.after(200, lambda: self.attributes("-topmost", False))
        self.focus_force()

        ctk.CTkLabel(
            self,
            text="Register New User",
            font=("Arial", 22, "bold")
        ).pack(pady=20)

        self.name_entry = ctk.CTkEntry(
            self,
            width=300,
            placeholder_text="Enter Your Name"
        )
        self.name_entry.pack(pady=20)

        ctk.CTkButton(
            self,
            text="Start Registration",
            command=self.start_registration
        ).pack(pady=20)

    def start_registration(self):

        username = self.name_entry.get().strip()

        if username == "":
            messagebox.showwarning(
                "Warning",
                "Please enter your name."
            )
            return

        self.destroy()
        register_face(username)


def open_register_window():

    window = RegisterWindow()
    window.grab_set()
    return window