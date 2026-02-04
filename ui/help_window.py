"""
TaskShot Help Window - Help and keyboard shortcuts reference
"""

import tkinter as tk
from tkinter import ttk
from ui.styled_button import create_styled_button

# Brand Colors
PRIMARY_PURPLE = "#a23b84"
SECONDARY_PURPLE = "#3a2b95"
ACCENT_PURPLE = "#6f2fa6"
DARK_BG = "#1a1a1a"
LIGHT_TEXT = "#ffffff"
MUTED_TEXT = "#b0b0b0"


class HelpWindow:
    """Help and keyboard shortcuts window"""

    def __init__(self, parent):
        self.parent = parent
        self.setup_window()
        self.setup_ui()

    def setup_window(self):
        """Configure the help window"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("TaskShot Help")
        self.window.configure(bg=DARK_BG)
        self.window.geometry("600x700")
        self.window.resizable(True, True)

        # Center on screen
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"+{x}+{y}")

    def setup_ui(self):
        """Set up the help UI"""
        # Main scrollable container
        canvas = tk.Canvas(self.window, bg=DARK_BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.window, orient='vertical', command=canvas.yview)
        main_frame = tk.Frame(canvas, bg=DARK_BG)

        main_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )

        canvas.create_window((0, 0), window=main_frame, anchor='nw', width=580)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)

        # Enable mousewheel scrolling
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        # Content
        content_frame = tk.Frame(main_frame, bg=DARK_BG, padx=30, pady=20)
        content_frame.pack(fill='both', expand=True)

        # Title
        title = tk.Label(
            content_frame,
            text="Welcome to TaskShot",
            font=('Arial', 24, 'bold'),
            fg=LIGHT_TEXT,
            bg=DARK_BG
        )
        title.pack(pady=(0, 20))

        # Description
        desc = tk.Label(
            content_frame,
            text="TaskShot is an open-source, accessible screenshot documentation tool\n"
                 "designed with Universal Design for Learning (UDL) and\n"
                 "WCAG 2.1 AA compliance at its core.",
            font=('Arial', 12),
            fg=MUTED_TEXT,
            bg=DARK_BG,
            justify='center'
        )
        desc.pack(pady=(0, 30))

        # How to Use section
        self.create_section(content_frame, "How to Use")

        steps = [
            "1. Enter a name for your task/tutorial",
            "2. Click \"Start Capture\" or press Ctrl+Shift+S",
            "3. Click through your process - each click captures a screenshot",
            "4. Click \"Stop Capture\" or press Ctrl+Shift+X when done",
            "5. Review and label each step",
            "6. Generate your accessible Word document"
        ]

        for step in steps:
            self.create_text(content_frame, step)

        # Keyboard Shortcuts section
        self.create_section(content_frame, "Keyboard Shortcuts")

        shortcuts = [
            ("Ctrl+Shift+S (Cmd+Shift+S on Mac)", "Start capture"),
            ("Ctrl+Shift+X (Cmd+Shift+X on Mac)", "Stop capture"),
            ("Ctrl+Shift+H (Cmd+Shift+H on Mac)", "Show this help"),
            ("Ctrl+Shift+E (Cmd+Shift+E on Mac)", "Open settings"),
            ("Arrow keys", "Navigate screenshots in review mode"),
            ("Enter", "Next field in review mode"),
            ("Delete", "Remove selected screenshot")
        ]

        self.create_shortcut_table(content_frame, shortcuts)

        # Accessibility Features section
        self.create_section(content_frame, "Accessibility Features")

        features = [
            "Full keyboard navigation",
            "Screen reader compatible",
            "High contrast dark theme",
            "Manual alt text entry for accessibility",
            "WCAG 2.1 AA compliant document output",
            "Customizable visual and audio feedback"
        ]

        for feature in features:
            self.create_checkmark(content_frame, feature)

        # Permissions section
        self.create_section(content_frame, "Permissions (macOS)")

        permissions_text = (
            "If screen capture fails, you may need to grant permissions:\n\n"
            "1. Open System Preferences > Security & Privacy\n"
            "2. Click the Privacy tab\n"
            "3. Select Screen Recording from the left sidebar\n"
            "4. Check the box next to TaskShot\n"
            "5. Restart TaskShot"
        )

        self.create_text(content_frame, permissions_text, indent=False)

        # Credits section
        self.create_section(content_frame, "Credits")

        credits_text = (
            "Made by Rocco Catrone of Tech Inclusion Pro\n"
            "Licensed under MIT License - Free and Open Source\n\n"
            "For support or to contribute:\n"
            "https://github.com/TechInclusionPro/TaskShot"
        )

        self.create_text(content_frame, credits_text, indent=False)

        # Close button
        close_btn = create_styled_button(
            content_frame,
            text="Close",
            command=self.window.destroy,
            font=('Arial', 12),
            padx=30,
            pady=8
        )
        close_btn.pack(pady=30)

    def create_section(self, parent, title):
        """Create a section header"""
        separator = tk.Frame(parent, bg=ACCENT_PURPLE, height=2)
        separator.pack(fill='x', pady=(25, 5))

        label = tk.Label(
            parent,
            text=title,
            font=('Arial', 16, 'bold'),
            fg=PRIMARY_PURPLE,
            bg=DARK_BG,
            anchor='w'
        )
        label.pack(fill='x', pady=(5, 15))

    def create_text(self, parent, text, indent=True):
        """Create a text paragraph"""
        label = tk.Label(
            parent,
            text=text,
            font=('Arial', 11),
            fg=LIGHT_TEXT if indent else MUTED_TEXT,
            bg=DARK_BG,
            anchor='w',
            justify='left'
        )
        label.pack(fill='x', pady=3, padx=(20 if indent else 0, 0))

    def create_checkmark(self, parent, text):
        """Create a checkmark item"""
        label = tk.Label(
            parent,
            text=f"  {text}",
            font=('Arial', 11),
            fg=LIGHT_TEXT,
            bg=DARK_BG,
            anchor='w'
        )
        label.pack(fill='x', pady=3, padx=20)

    def create_shortcut_table(self, parent, shortcuts):
        """Create a keyboard shortcut table"""
        table_frame = tk.Frame(parent, bg='#252525', padx=10, pady=10)
        table_frame.pack(fill='x', pady=10)

        for shortcut, description in shortcuts:
            row_frame = tk.Frame(table_frame, bg='#252525')
            row_frame.pack(fill='x', pady=3)

            key_label = tk.Label(
                row_frame,
                text=shortcut,
                font=('Courier New', 10, 'bold'),
                fg=PRIMARY_PURPLE,
                bg='#252525',
                width=35,
                anchor='w'
            )
            key_label.pack(side='left')

            desc_label = tk.Label(
                row_frame,
                text=description,
                font=('Arial', 10),
                fg=LIGHT_TEXT,
                bg='#252525',
                anchor='w'
            )
            desc_label.pack(side='left', fill='x', expand=True)
