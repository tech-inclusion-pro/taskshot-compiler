"""
TaskShot Control Bar - Floating toolbar for capture control
"""

import tkinter as tk
from tkinter import ttk
from ui.styled_button import create_styled_button, apply_hover_to_button, PRIMARY_PURPLE

# Brand Colors
DARK_BG = "#1a1a1a"
LIGHT_TEXT = "#ffffff"
MUTED_TEXT = "#b0b0b0"


class ControlBar:
    """Floating control bar for screenshot capture"""

    def __init__(self, root, task_name, on_start, on_stop, on_settings, on_help):
        self.root = root
        self.task_name = task_name
        self.on_start = on_start
        self.on_stop = on_stop
        self.on_settings = on_settings
        self.on_help = on_help
        self.screenshot_count = 0

        self.setup_window()
        self.setup_ui()

    def setup_window(self):
        """Configure the control bar window"""
        self.root.title(f"TaskShot - {self.task_name}")
        self.root.configure(bg=DARK_BG)
        self.root.attributes('-topmost', True)
        self.root.resizable(False, False)

        # Position at top center of screen
        window_width = 650
        window_height = 80
        screen_width = self.root.winfo_screenwidth()
        x = (screen_width - window_width) // 2
        y = 10

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def setup_ui(self):
        """Set up the control bar UI"""
        # Main container
        self.main_frame = tk.Frame(self.root, bg=DARK_BG, padx=15, pady=10)
        self.main_frame.pack(fill='both', expand=True)

        # Task name label
        self.task_label = tk.Label(
            self.main_frame,
            text=f"Task: {self.task_name}",
            font=('Arial', 11),
            fg=MUTED_TEXT,
            bg=DARK_BG
        )
        self.task_label.pack(side='left', padx=(0, 20))

        # Start button (rounded)
        self.start_btn = create_styled_button(
            self.main_frame,
            text="Start Capture",
            command=self.on_start,
            font=('Arial', 12, 'bold'),
            padx=15,
            pady=8
        )
        self.start_btn.pack(side='left', padx=5)

        # Stop button (rounded, disabled initially)
        self.stop_btn = create_styled_button(
            self.main_frame,
            text="Stop Capture",
            command=self.on_stop,
            font=('Arial', 12, 'bold'),
            padx=15,
            pady=8
        )
        self.stop_btn.pack(side='left', padx=5)
        self.stop_btn.configure(state='disabled')

        # Screenshot counter
        self.count_label = tk.Label(
            self.main_frame,
            text="Screenshots: 0",
            font=('Arial', 12, 'bold'),
            fg=LIGHT_TEXT,
            bg=DARK_BG
        )
        self.count_label.pack(side='left', padx=20)

        # Right side buttons frame
        right_frame = tk.Frame(self.main_frame, bg=DARK_BG)
        right_frame.pack(side='right')

        # Settings button (rounded)
        self.settings_btn = create_styled_button(
            right_frame,
            text="Settings",
            command=self.on_settings,
            font=('Arial', 10),
            padx=10,
            pady=5
        )
        self.settings_btn.pack(side='left', padx=3)

        # Help button (rounded)
        self.help_btn = create_styled_button(
            right_frame,
            text="Help",
            command=self.on_help,
            font=('Arial', 10),
            padx=10,
            pady=5
        )
        self.help_btn.pack(side='left', padx=3)

    def set_capturing(self, is_capturing):
        """Update UI based on capture state"""
        if is_capturing:
            self.start_btn.configure(state='disabled')
            self.stop_btn.configure(state='normal')
        else:
            self.start_btn.configure(state='normal')
            self.stop_btn.configure(state='disabled')

    def update_count(self, count):
        """Update the screenshot counter"""
        self.screenshot_count = count
        self.count_label.configure(text=f"Screenshots: {count}")
