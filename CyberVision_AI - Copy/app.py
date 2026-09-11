import tkinter as tk
from tkinter import messagebox
from PIL import Image,ImageTk
import threading
import cv2

from modules.register_window import open_register_window
from modules.scan_face import scan_face
from modules.privacy_guard import privacy_guard


# ----------------------------------
# Functions
# ----------------------------------

def register_face():
    open_register_window()


def start_scan():
    threading.Thread(
        target=scan_face,
        daemon=True
    ).start()


def start_privacy():
    threading.Thread(
        target=privacy_guard,
        daemon=True
    ).start()


def exit_app():

    if messagebox.askyesno(
        "Exit",
        "Are you sure you want to exit CyberVision AI?"
    ):
        cv2.destroyAllWindows()
        root.destroy()


# ----------------------------------
# Camera Status
# ----------------------------------

def update_camera_status():

    cap = cv2.VideoCapture(0)
    try:
        if cap.isOpened():
            status_label.config(
            text="🟢 Camera Connected",
            fg="#00FF66"
        )
        else:
            status_label.config(
            text="🔴 Camera Not Found",
            fg="red"
        )
    finally:
        cap.release()

    


# ----------------------------------
# Main Window
# ----------------------------------

root = tk.Tk()


root.title("CyberVision Security")

root.geometry("900x600")

root.configure(
    bg="#000000"
)

root.resizable(
    False,
    False
)
root.withdraw()


# ----------------------------------
# Header
# ----------------------------------

title = tk.Label(

    root,

    text="CYBERVISION SECURITY",

    font=("Segoe UI", 28, "bold"),

    fg="#38BDF8",

    bg="#0F172A"

)

title.pack(
    pady=(20, 5)
)


subtitle = tk.Label(

    root,

    text="Privacy Protection System",

    font=("Segoe UI", 12),

    fg="white",

    bg="#0F172A"

)

subtitle.pack()


# ----------------------------------
# Status Frame
# ----------------------------------

status_frame = tk.Frame(

    root,

    bg="#1E293B",

    bd=2,

    relief="ridge"

)

status_frame.pack(

    pady=20,

    padx=20,

    fill="x"

)

status_label = tk.Label(

    status_frame,

    text="Checking Camera...Please Wait...",

    font=("Segoe UI", 12, "bold"),

    fg="white",

    bg="#1E293B"

)

status_label.pack(

    pady=10
)


version_label = tk.Label(

    status_frame,

    text="Version : 1.0",

    font=("Segoe UI", 11),

    fg="lightgray",

    bg="#1E293B"

)

version_label.pack(
    pady=(0, 10)
)


# ----------------------------------
# Button Frame
# ----------------------------------

button_frame = tk.Frame(

    root,

    bg="#0F172A"

)

button_frame.pack(
    pady=20
)
# ----------------------------------
# Buttons
# ----------------------------------

btn_register = tk.Button(
    button_frame,
    text="📷 Register Face",
    font=("Segoe UI", 14, "bold"),
    width=24,
    height=2,
    bg="#2563EB",
    fg="white",
    activebackground="#1D4ED8",
    command=register_face
)

btn_register.grid(
    row=0,
    column=0,
    padx=15,
    pady=15
)


btn_scan = tk.Button(
    button_frame,
    text="👁 Scan Face",
    font=("Segoe UI", 14, "bold"),
    width=22,
    height=2,
    bg="#16A34A",
    fg="white",
    activebackground="#15803D",
    command=start_scan
)

btn_scan.grid(
    row=0,
    column=1,
    padx=15,
    pady=15
)


btn_privacy = tk.Button(
    button_frame,
    text="🛡 Privacy Guard",
    font=("Segoe UI", 14, "bold"),
    width=22,
    height=2,
    bg="#DC2626",
    fg="white",
    activebackground="#B91C1C",
    command=start_privacy
)

btn_privacy.grid(
    row=1,
    column=0,
    padx=15,
    pady=15
)


def open_logs():
    messagebox.showinfo(
        "Logs",
        "Logs are available in:\n\nlogs/events.log"
    )


btn_logs = tk.Button(
    button_frame,
    text="📜 View Logs",
    font=("Segoe UI", 14, "bold"),
    width=22,
    height=2,
    bg="#7C3AED",
    fg="white",
    activebackground="#6D28D9",
    command=open_logs
)

btn_logs.grid(
    row=1,
    column=1,
    padx=15,
    pady=15
)


btn_exit = tk.Button(
    root,
    text="❌ Exit",
    font=("Segoe UI", 13, "bold"),
    width=20,
    height=2,
    bg="#374151",
    fg="white",
    activebackground="#1F2937",
    command=exit_app
)

btn_exit.pack(
    pady=20
)


# ----------------------------------
# Footer
# ----------------------------------

footer = tk.Label(
    root,
    text="CyberVision Security",
    font=("Segoe UI", 10),
    fg="lightgray",
    bg="#0F172A"
)

footer.pack(
    side="bottom",
    pady=12
)


# ----------------------------------
# Start Camera Status
# ----------------------------------


def show_splash():

    splash = tk.Toplevel()
    splash.overrideredirect(True)
    splash.configure(bg="#1e1f22")

    w = 420
    h = 320

    sw = splash.winfo_screenwidth()
    sh = splash.winfo_screenheight()

    x = (sw - w) // 2
    y = (sh - h) // 2

    splash.geometry(f"{w}x{h}+{x}+{y}")

    logo = Image.open("logo.jpeg").convert("RGBA")
    logo = logo.resize((120,120), Image.LANCZOS)

    label = tk.Label(
        splash,
        bg="#1e1f22"
    )

    label.pack(pady=60)

    tk.Label(
        splash,
        text="CYBERVISION SECURITY",
        fg="white",
        bg="#1e1f22",
        font=("Segoe UI", 22, "bold")
    ).pack()
    tk.Label(
        splash,
        text="Loading...",
        fg="#38BDF8",
        bg="#0F172A",
        font=("Segoe UI",12)
    ).pack(pady=10)

    angle = 0

    def animate():

        nonlocal angle

        img = logo.rotate(
            angle,
            resample=Image.BICUBIC,
            expand=True
        )

        photo = ImageTk.PhotoImage(img)

        label.configure(image=photo)

        label.image = photo

        angle = (angle + 5) % 360

        splash.after(
            30,
            animate
        )

    animate()

    def close():
         splash.destroy()
         root.update_idletasks()
         root.deiconify()
         root.update()
         update_camera_status()



    splash.after(
        2000,
        close
    )

# ----------------------------------
# Run App
# ----------------------------------
show_splash()
root.mainloop()