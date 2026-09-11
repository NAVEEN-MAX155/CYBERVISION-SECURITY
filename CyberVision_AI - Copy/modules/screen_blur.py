import tkinter as tk
from PIL import ImageGrab, ImageFilter, ImageTk


class ScreenBlur:

    def __init__(self):

        self.root = None


    # =================================================
    # SHOW BLUR
    # =================================================

    def show(
        self,
        title="🔒 PRIVACY MODE",
        subtitle="Unauthorized Person Detected"
    ):

        if self.root is not None:
            return


        self.root = tk.Toplevel()


        # ---------------------------------------------
        # Fullscreen
        # ---------------------------------------------

        self.root.attributes(
            "-fullscreen",
            True
        )

        self.root.attributes(
            "-topmost",
            True
        )

        self.root.overrideredirect(
            True
        )


        # Prevent closing
        self.root.protocol(
            "WM_DELETE_WINDOW",
            lambda: None
        )


        # ---------------------------------------------
        # Screenshot
        # ---------------------------------------------

        try:

            img = ImageGrab.grab()


            img = img.filter(
                ImageFilter.GaussianBlur(
                    radius=20
                )
            )


            photo = ImageTk.PhotoImage(
                img
            )


        except Exception as e:

            print(
                "Screen Blur Error:",
                e
            )


            self.root.destroy()

            self.root = None

            return


        # ---------------------------------------------
        # Canvas
        # ---------------------------------------------

        canvas = tk.Canvas(

            self.root,

            highlightthickness=0,

            bd=0

        )


        canvas.pack(
            fill="both",
            expand=True
        )


        canvas.create_image(

            0,

            0,

            anchor="nw",

            image=photo

        )


        canvas.image = photo


        # ---------------------------------------------
        # Center
        # ---------------------------------------------

        width = (
            self.root.winfo_screenwidth()
        )

        height = (
            self.root.winfo_screenheight()
        )


        center_x = width // 2

        center_y = height // 2


        # ---------------------------------------------
        # Title
        # ---------------------------------------------

        canvas.create_text(

            center_x,

            center_y - 45,

            text=title,

            fill="white",

            font=(
                "Segoe UI",
                30,
                "bold"
            )

        )


        # ---------------------------------------------
        # Subtitle
        # ---------------------------------------------

        canvas.create_text(

            center_x,

            center_y + 20,

            text=subtitle,

            fill="#38BDF8",

            font=(
                "Segoe UI",
                18,
                "bold"
            )

        )


        # ---------------------------------------------
        # Block mouse
        # ---------------------------------------------

        mouse_events = (

            "<Button-1>",

            "<Button-2>",

            "<Button-3>",

            "<Double-Button-1>",

            "<MouseWheel>",

            "<Motion>"

        )


        for event in mouse_events:

            self.root.bind(

                event,

                lambda e: "break"

            )


        # ---------------------------------------------
        # Block keyboard
        # ---------------------------------------------

        self.root.bind(

            "<Key>",

            lambda e: "break"

        )


        self.root.bind(

            "<KeyPress>",

            lambda e: "break"

        )


        self.root.bind(

            "<KeyRelease>",

            lambda e: "break"

        )


        # ---------------------------------------------
        # Focus
        # ---------------------------------------------

        self.root.focus_force()


        try:

            self.root.grab_set()

        except tk.TclError:

            pass


        self.root.update()


    # =================================================
    # HIDE BLUR
    # =================================================

    def hide(self):

        if self.root is None:
            return


        try:

            self.root.grab_release()

        except tk.TclError:

            pass


        try:

            self.root.destroy()

        except tk.TclError:

            pass


        self.root = None


# =====================================================
# GLOBAL OBJECT
# =====================================================

blur = ScreenBlur()