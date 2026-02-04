#!/usr/bin/env python3
"""
TaskShot - Accessible Screenshot Documentation Tool
Made by Rocco Catrone of Tech Inclusion Pro
Licensed under MIT License - Free and Open Source
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import json
import sys
import time
from datetime import datetime

# Add the app directory to path for imports
APP_DIR = Path(__file__).parent
sys.path.insert(0, str(APP_DIR))

from PIL import Image, ImageTk, ImageDraw
from ui.control_bar import ControlBar
from ui.review_window import ReviewWindow
from ui.settings_window import SettingsWindow
from ui.help_window import HelpWindow
from ui.styled_button import create_styled_button, apply_hover_to_button
from capture.screenshot import ScreenshotCapture
from capture.mouse_listener import MouseListener
from document.docx_builder import DocxBuilder
from config.settings import Settings

# Brand Colors
PRIMARY_PURPLE = "#a23b84"
SECONDARY_PURPLE = "#3a2b95"
ACCENT_PURPLE = "#6f2fa6"
DARK_BG = "#1a1a1a"
LIGHT_TEXT = "#ffffff"
MUTED_TEXT = "#b0b0b0"


class SplashScreen:
    """Login/Splash screen for TaskShot"""

    def __init__(self, root, on_continue, settings=None):
        self.root = root
        self.on_continue = on_continue
        self.settings = settings or Settings()
        self.root.title("TaskShot - Accessible Screenshot Documentation")
        self.root.configure(bg=DARK_BG)
        self.root.resizable(False, False)

        # Center window on screen
        window_width = 500
        window_height = 800
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.setup_ui()

    def setup_ui(self):
        """Set up the splash screen UI"""
        # Main scrollable container
        canvas = tk.Canvas(self.root, bg=DARK_BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.root, orient='vertical', command=canvas.yview)
        self.main_frame = tk.Frame(canvas, bg=DARK_BG, padx=20)

        self.main_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )

        # Width: 500 (window) - 20 (scrollbar) - 40 (padding) = 440
        canvas.create_window((0, 0), window=self.main_frame, anchor='nw', width=440)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True, padx=10, pady=10)

        # Logo section
        self.load_logo()

        # App title
        title_label = tk.Label(
            self.main_frame,
            text="TaskShot",
            font=('Arial', 32, 'bold'),
            fg=LIGHT_TEXT,
            bg=DARK_BG
        )
        title_label.pack(pady=(20, 5))

        # Subtitle
        subtitle_label = tk.Label(
            self.main_frame,
            text="Accessible Screenshot Documentation Tool",
            font=('Arial', 14),
            fg=MUTED_TEXT,
            bg=DARK_BG
        )
        subtitle_label.pack(pady=(0, 20))

        # Task name input section
        task_frame = tk.Frame(self.main_frame, bg=DARK_BG)
        task_frame.pack(fill='x', pady=10)

        task_label = tk.Label(
            task_frame,
            text="Enter Task Name:",
            font=('Arial', 14),
            fg=LIGHT_TEXT,
            bg=DARK_BG,
            anchor='w'
        )
        task_label.pack(fill='x', pady=(0, 8))

        # Task name entry with styling
        entry_frame = tk.Frame(task_frame, bg=ACCENT_PURPLE, padx=2, pady=2)
        entry_frame.pack(fill='x')

        self.task_name_var = tk.StringVar()
        self.task_entry = tk.Entry(
            entry_frame,
            textvariable=self.task_name_var,
            font=('Arial', 14),
            bg='#2a2a2a',
            fg=LIGHT_TEXT,
            insertbackground=LIGHT_TEXT,
            relief='flat'
        )
        self.task_entry.pack(fill='x', padx=2, pady=2, ipady=10)
        self.task_entry.focus_set()

        # Bind Enter key
        self.task_entry.bind('<Return>', lambda e: self.start_capture())

        # Hint text
        hint_label = tk.Label(
            task_frame,
            text="This name will be used for your document filename",
            font=('Arial', 10),
            fg=MUTED_TEXT,
            bg=DARK_BG
        )
        hint_label.pack(pady=(5, 0), anchor='w')

        # Start button with hover effect
        self.start_btn = create_styled_button(
            self.main_frame,
            text="Start Capture",
            command=self.start_capture,
            font=('Arial', 16, 'bold'),
            padx=40,
            pady=15
        )
        self.start_btn.pack(pady=20)

        # Keyboard shortcut hint
        shortcut_label = tk.Label(
            self.main_frame,
            text="Keyboard Shortcut: Ctrl+Shift+S to start capture",
            font=('Arial', 11),
            fg=MUTED_TEXT,
            bg=DARK_BG
        )
        shortcut_label.pack(pady=(0, 15))

        # Features list
        features_frame = tk.Frame(self.main_frame, bg='#252525', padx=15, pady=15)
        features_frame.pack(fill='x', pady=10)

        features_title = tk.Label(
            features_frame,
            text="Features:",
            font=('Arial', 12, 'bold'),
            fg=LIGHT_TEXT,
            bg='#252525',
            anchor='w'
        )
        features_title.pack(fill='x', pady=(0, 10))

        features = [
            "Full keyboard navigation",
            "Screen reader compatible",
            "Manual alt text entry for accessibility",
            "WCAG 2.1 AA compliant output"
        ]

        for feature in features:
            feature_label = tk.Label(
                features_frame,
                text=f"  {feature}",
                font=('Arial', 11),
                fg=MUTED_TEXT,
                bg='#252525',
                anchor='w'
            )
            feature_label.pack(fill='x', pady=2)

        # Credits
        credits_label = tk.Label(
            self.main_frame,
            text="Made by Rocco Catrone of Tech Inclusion Pro",
            font=('Arial', 10),
            fg=MUTED_TEXT,
            bg=DARK_BG
        )
        credits_label.pack(pady=(20, 10))

    def load_logo(self):
        """Load and display the logo"""
        try:
            logo_path = APP_DIR / "assets" / "icons" / "taskshot_icon.png"
            if logo_path.exists():
                img = Image.open(logo_path)
                img = img.resize((150, 150), Image.Resampling.LANCZOS)
                self.logo_image = ImageTk.PhotoImage(img)

                logo_label = tk.Label(
                    self.main_frame,
                    image=self.logo_image,
                    bg=DARK_BG
                )
                logo_label.pack(pady=(0, 10))
        except Exception as e:
            print(f"Could not load logo: {e}")

    def start_capture(self):
        """Validate and start the capture process"""
        task_name = self.task_name_var.get().strip()
        if not task_name:
            messagebox.showwarning(
                "Task Name Required",
                "Please enter a task name before starting capture."
            )
            self.task_entry.focus_set()
            return

        # Validate filename characters
        invalid_chars = '<>:"/\\|?*'
        if any(char in task_name for char in invalid_chars):
            messagebox.showwarning(
                "Invalid Characters",
                f"Task name cannot contain: {invalid_chars}"
            )
            return

        self.on_continue(task_name)


class TaskShotApp:
    """Main TaskShot Application"""

    def __init__(self):
        self.root = tk.Tk()
        self.settings = Settings()
        self.screenshots = []
        self.is_capturing = False
        self.task_name = ""
        self.mouse_listener = None
        self.screenshot_capture = ScreenshotCapture(self.settings)

        # Set up the splash screen first
        self.splash = SplashScreen(self.root, self.on_splash_continue, self.settings)

    def on_splash_continue(self, task_name):
        """Called when user clicks Start Capture on splash screen"""
        self.task_name = task_name

        # Clear splash screen
        for widget in self.root.winfo_children():
            widget.destroy()

        # Show control bar
        self.show_control_bar()

    def show_control_bar(self):
        """Show the always-on-top control bar"""
        self.control_bar = ControlBar(
            self.root,
            task_name=self.task_name,
            on_start=self.start_capture,
            on_stop=self.stop_capture,
            on_settings=self.show_settings,
            on_help=self.show_help
        )

        # Auto-start capture
        self.start_capture()

    def start_capture(self):
        """Start the screenshot capture process"""
        if self.is_capturing:
            return

        self.is_capturing = True
        self.screenshots = []
        self.control_bar.set_capturing(True)

        # Start mouse listener
        self.mouse_listener = MouseListener(
            on_click=self.on_mouse_click,
            settings=self.settings
        )
        self.mouse_listener.start()

        # Minimize main window
        self.root.iconify()

    def stop_capture(self):
        """Stop the screenshot capture process"""
        if not self.is_capturing:
            return

        self.is_capturing = False
        self.control_bar.set_capturing(False)

        # Stop mouse listener
        if self.mouse_listener:
            self.mouse_listener.stop()
            self.mouse_listener = None

        # Restore window
        self.root.deiconify()

        # Show review window
        if self.screenshots:
            self.show_review_window()
        else:
            messagebox.showinfo(
                "No Screenshots",
                "No screenshots were captured. Start a new capture session?"
            )
            self.show_splash()

    def on_mouse_click(self, x, y, button):
        """Handle mouse click during capture"""
        if not self.is_capturing:
            return

        # Capture screenshot
        screenshot_data = self.screenshot_capture.capture(x, y)
        if screenshot_data:
            self.screenshots.append(screenshot_data)
            # Schedule UI update on main thread (tkinter is not thread-safe)
            count = len(self.screenshots)
            self.root.after(0, lambda c=count: self.control_bar.update_count(c))

    def show_review_window(self):
        """Show the screenshot review window"""
        review_window = ReviewWindow(
            self.root,
            screenshots=self.screenshots,
            task_name=self.task_name,
            on_generate=self.generate_document,
            on_cancel=self.show_splash,
            settings=self.settings
        )

    def generate_document(self, screenshots, task_name):
        """Generate the Word document"""
        builder = DocxBuilder(self.settings)

        try:
            output_path = builder.create_document(screenshots, task_name)
            messagebox.showinfo(
                "Document Created",
                f"Your accessible document has been created:\n{output_path}"
            )
        except Exception as e:
            self.handle_document_error(e, screenshots, task_name)

        self.show_splash()

    def handle_document_error(self, error, screenshots, task_name):
        """Handle document generation errors"""
        result = messagebox.askyesno(
            "Document Generation Failed",
            f"Unable to create Word document: {error}\n\n"
            "Would you like to copy the content to clipboard as markdown instead?"
        )

        if result:
            markdown = self.generate_markdown(screenshots, task_name)
            self.root.clipboard_clear()
            self.root.clipboard_append(markdown)
            messagebox.showinfo(
                "Copied",
                "Content has been copied to clipboard in markdown format."
            )

    def generate_markdown(self, screenshots, task_name):
        """Generate markdown version of the tutorial"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        lines = [
            f"# {task_name} Tutorial",
            f"Created: {date_str}",
            "Made by Rocco Catrone of Tech Inclusion Pro",
            ""
        ]

        for i, ss in enumerate(screenshots, 1):
            lines.append(f"## Step {i}: {ss.get('title', 'Untitled')}")
            lines.append(f"![Screenshot {i} - Alt text: {ss.get('alt_text', 'No description')}]")
            if ss.get('notes'):
                lines.append(f"Notes: {ss['notes']}")
            lines.append("")

        return "\n".join(lines)

    def show_splash(self):
        """Return to splash screen"""
        for widget in self.root.winfo_children():
            widget.destroy()
        self.splash = SplashScreen(self.root, self.on_splash_continue, self.settings)

    def show_settings(self):
        """Show settings window"""
        SettingsWindow(self.root, self.settings)

    def show_help(self):
        """Show help window"""
        HelpWindow(self.root)

    def run(self):
        """Start the application"""
        self.root.mainloop()


def main():
    """Main entry point"""
    app = TaskShotApp()
    app.run()


if __name__ == "__main__":
    main()
