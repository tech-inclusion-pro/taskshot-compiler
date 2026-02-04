"""
TaskShot Settings Window - Application configuration interface
"""

import tkinter as tk
from tkinter import ttk, colorchooser, messagebox
from ui.styled_button import create_styled_button, apply_hover_to_button

# Brand Colors
PRIMARY_PURPLE = "#a23b84"
SECONDARY_PURPLE = "#3a2b95"
ACCENT_PURPLE = "#6f2fa6"
DARK_BG = "#1a1a1a"
LIGHT_TEXT = "#ffffff"
MUTED_TEXT = "#b0b0b0"
HOVER_BLACK = "#000000"


class SettingsWindow:
    """Settings configuration window"""

    def __init__(self, parent, settings):
        self.parent = parent
        self.settings = settings

        self.setup_window()
        self.setup_ui()
        self.load_settings()

    def setup_window(self):
        """Configure the settings window"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("TaskShot Settings")
        self.window.configure(bg=DARK_BG)
        self.window.geometry("500x700")
        self.window.resizable(False, False)

        # Center on screen
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"+{x}+{y}")

        # Make modal
        self.window.transient(self.parent)
        self.window.grab_set()

    def setup_ui(self):
        """Set up the settings UI"""
        # Main scrollable container
        canvas = tk.Canvas(self.window, bg=DARK_BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.window, orient='vertical', command=canvas.yview)
        main_frame = tk.Frame(canvas, bg=DARK_BG)

        main_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )

        canvas.create_window((0, 0), window=main_frame, anchor='nw', width=480)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)

        # Title
        title_label = tk.Label(
            main_frame,
            text="Settings",
            font=('Arial', 20, 'bold'),
            fg=LIGHT_TEXT,
            bg=DARK_BG
        )
        title_label.pack(pady=20)

        # === Capture Settings Section ===
        self.create_section(main_frame, "Capture Settings")

        # Sound feedback checkbox
        self.sound_var = tk.BooleanVar()
        self.create_checkbox(main_frame, "Enable sound feedback", self.sound_var)

        # Visual flash checkbox
        self.flash_var = tk.BooleanVar()
        self.create_checkbox(main_frame, "Enable visual flash", self.flash_var)

        # Circle color picker
        color_frame = tk.Frame(main_frame, bg=DARK_BG)
        color_frame.pack(fill='x', padx=30, pady=5)

        color_label = tk.Label(
            color_frame,
            text="Circle color:",
            font=('Arial', 11),
            fg=LIGHT_TEXT,
            bg=DARK_BG
        )
        color_label.pack(side='left')

        self.circle_color = "#FF0000"
        self.color_btn = tk.Button(
            color_frame,
            text="      ",
            bg=self.circle_color,
            relief='flat',
            cursor='hand2',
            command=self.choose_circle_color
        )
        self.color_btn.pack(side='left', padx=10)

        # Circle size slider
        size_frame = tk.Frame(main_frame, bg=DARK_BG)
        size_frame.pack(fill='x', padx=30, pady=10)

        size_label = tk.Label(
            size_frame,
            text="Circle size:",
            font=('Arial', 11),
            fg=LIGHT_TEXT,
            bg=DARK_BG
        )
        size_label.pack(anchor='w')

        self.size_var = tk.IntVar(value=40)
        size_slider = tk.Scale(
            size_frame,
            from_=20,
            to=80,
            orient='horizontal',
            variable=self.size_var,
            bg=DARK_BG,
            fg=LIGHT_TEXT,
            highlightthickness=0,
            troughcolor='#333333',
            activebackground=PRIMARY_PURPLE
        )
        size_slider.pack(fill='x')

        # === Document Settings Section ===
        self.create_section(main_frame, "Document Settings")

        # Header color picker
        header_frame = tk.Frame(main_frame, bg=DARK_BG)
        header_frame.pack(fill='x', padx=30, pady=5)

        header_label = tk.Label(
            header_frame,
            text="Header color:",
            font=('Arial', 11),
            fg=LIGHT_TEXT,
            bg=DARK_BG
        )
        header_label.pack(side='left')

        self.header_color = PRIMARY_PURPLE
        self.header_color_btn = tk.Button(
            header_frame,
            text="      ",
            bg=self.header_color,
            relief='flat',
            cursor='hand2',
            command=self.choose_header_color
        )
        self.header_color_btn.pack(side='left', padx=10)

        # Table border color picker
        border_frame = tk.Frame(main_frame, bg=DARK_BG)
        border_frame.pack(fill='x', padx=30, pady=5)

        border_label = tk.Label(
            border_frame,
            text="Table border color:",
            font=('Arial', 11),
            fg=LIGHT_TEXT,
            bg=DARK_BG
        )
        border_label.pack(side='left')

        self.border_color = ACCENT_PURPLE
        self.border_color_btn = tk.Button(
            border_frame,
            text="      ",
            bg=self.border_color,
            relief='flat',
            cursor='hand2',
            command=self.choose_border_color
        )
        self.border_color_btn.pack(side='left', padx=10)

        # Footer accessibility statement checkbox
        self.footer_var = tk.BooleanVar(value=True)
        self.create_checkbox(main_frame, "Include footer accessibility statement", self.footer_var)

        # Margin size dropdown
        margin_frame = tk.Frame(main_frame, bg=DARK_BG)
        margin_frame.pack(fill='x', padx=30, pady=10)

        margin_label = tk.Label(
            margin_frame,
            text="Margin size:",
            font=('Arial', 11),
            fg=LIGHT_TEXT,
            bg=DARK_BG
        )
        margin_label.pack(side='left')

        self.margin_var = tk.StringVar(value='0.5"')
        margin_dropdown = ttk.Combobox(
            margin_frame,
            textvariable=self.margin_var,
            values=['0.5"', '0.75"', '1"'],
            state='readonly',
            width=10
        )
        margin_dropdown.pack(side='left', padx=10)

        # === Buttons ===
        button_frame = tk.Frame(main_frame, bg=DARK_BG)
        button_frame.pack(fill='x', pady=30)

        save_btn = create_styled_button(
            button_frame,
            text="Save Settings",
            command=self.save_settings,
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=8
        )
        save_btn.pack(side='left', padx=30)

        cancel_btn = create_styled_button(
            button_frame,
            text="Cancel",
            command=self.window.destroy,
            font=('Arial', 12),
            padx=20,
            pady=8
        )
        cancel_btn.pack(side='right', padx=30)

    def create_section(self, parent, title):
        """Create a section header"""
        separator = tk.Frame(parent, bg=ACCENT_PURPLE, height=2)
        separator.pack(fill='x', padx=20, pady=(20, 5))

        label = tk.Label(
            parent,
            text=title,
            font=('Arial', 14, 'bold'),
            fg=PRIMARY_PURPLE,
            bg=DARK_BG
        )
        label.pack(anchor='w', padx=30, pady=(5, 10))

    def create_checkbox(self, parent, text, variable):
        """Create a styled checkbox"""
        frame = tk.Frame(parent, bg=DARK_BG)
        frame.pack(fill='x', padx=30, pady=5)

        cb = tk.Checkbutton(
            frame,
            text=text,
            variable=variable,
            font=('Arial', 11),
            fg=LIGHT_TEXT,
            bg=DARK_BG,
            activebackground=DARK_BG,
            activeforeground=LIGHT_TEXT,
            selectcolor='#333333'
        )
        cb.pack(anchor='w')

    def choose_circle_color(self):
        """Open color picker for circle color"""
        color = colorchooser.askcolor(color=self.circle_color, title="Choose Circle Color")
        if color[1]:
            self.circle_color = color[1]
            self.color_btn.configure(bg=self.circle_color)

    def choose_header_color(self):
        """Open color picker for header color"""
        color = colorchooser.askcolor(color=self.header_color, title="Choose Header Color")
        if color[1]:
            self.header_color = color[1]
            self.header_color_btn.configure(bg=self.header_color)

    def choose_border_color(self):
        """Open color picker for border color"""
        color = colorchooser.askcolor(color=self.border_color, title="Choose Border Color")
        if color[1]:
            self.border_color = color[1]
            self.border_color_btn.configure(bg=self.border_color)

    def load_settings(self):
        """Load current settings into UI"""
        self.sound_var.set(self.settings.get('sound_feedback', True))
        self.flash_var.set(self.settings.get('visual_flash', True))
        self.circle_color = self.settings.get('circle_color', '#FF0000')
        self.color_btn.configure(bg=self.circle_color)
        self.size_var.set(self.settings.get('circle_size', 40))
        self.header_color = self.settings.get('header_color', PRIMARY_PURPLE)
        self.header_color_btn.configure(bg=self.header_color)
        self.border_color = self.settings.get('border_color', ACCENT_PURPLE)
        self.border_color_btn.configure(bg=self.border_color)
        self.footer_var.set(self.settings.get('include_footer', True))
        self.margin_var.set(self.settings.get('margin_size', '0.5"'))

    def save_settings(self):
        """Save settings and close window"""
        self.settings.set('sound_feedback', self.sound_var.get())
        self.settings.set('visual_flash', self.flash_var.get())
        self.settings.set('circle_color', self.circle_color)
        self.settings.set('circle_size', self.size_var.get())
        self.settings.set('header_color', self.header_color)
        self.settings.set('border_color', self.border_color)
        self.settings.set('include_footer', self.footer_var.get())
        self.settings.set('margin_size', self.margin_var.get())
        self.settings.save()

        messagebox.showinfo("Settings Saved", "Your settings have been saved.")
        self.window.destroy()
