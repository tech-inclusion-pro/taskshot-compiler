"""
TaskShot Review Window - Screenshot review and editing interface
"""

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from pathlib import Path
from ui.styled_button import create_styled_button, apply_hover_to_button

# Brand Colors
PRIMARY_PURPLE = "#a23b84"
SECONDARY_PURPLE = "#3a2b95"
ACCENT_PURPLE = "#6f2fa6"
DARK_BG = "#1a1a1a"
LIGHT_TEXT = "#ffffff"
MUTED_TEXT = "#b0b0b0"
HOVER_BLACK = "#000000"


class ReviewWindow:
    """Window for reviewing and editing captured screenshots"""

    def __init__(self, parent, screenshots, task_name, on_generate, on_cancel, settings=None):
        self.parent = parent
        self.screenshots = screenshots
        self.task_name = task_name
        self.on_generate = on_generate
        self.on_cancel = on_cancel
        self.settings = settings
        self.current_index = 0
        self.thumbnail_images = []
        self.preview_image = None

        self.setup_window()
        self.setup_ui()
        self.load_thumbnails()
        self.select_screenshot(0)

    def setup_window(self):
        """Configure the review window"""
        self.window = tk.Toplevel(self.parent)
        self.window.title(f"Review Screenshots - {self.task_name}")
        self.window.configure(bg=DARK_BG)
        self.window.geometry("1200x800")
        self.window.attributes('-topmost', False)

        # Center on screen
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"+{x}+{y}")

        # Bind keyboard shortcuts
        self.window.bind('<Left>', lambda e: self.prev_screenshot())
        self.window.bind('<Right>', lambda e: self.next_screenshot())
        self.window.bind('<Delete>', lambda e: self.delete_screenshot())

        # Handle window close
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_ui(self):
        """Set up the review window UI"""
        # Main container
        main_frame = tk.Frame(self.window, bg=DARK_BG)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Top toolbar
        toolbar = tk.Frame(main_frame, bg=DARK_BG)
        toolbar.pack(fill='x', pady=(0, 10))

        # Generate Document button
        self.generate_btn = create_styled_button(
            toolbar,
            text="Generate Document",
            command=self.generate_document,
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=8
        )
        self.generate_btn.pack(side='left', padx=5)

        # Delete button
        self.delete_btn = create_styled_button(
            toolbar,
            text="Delete Selected",
            command=self.delete_screenshot,
            font=('Arial', 12),
            padx=15,
            pady=8
        )
        self.delete_btn.pack(side='left', padx=5)

        # Cancel button
        self.cancel_btn = create_styled_button(
            toolbar,
            text="Cancel",
            command=self.on_close,
            font=('Arial', 12),
            padx=15,
            pady=8
        )
        self.cancel_btn.pack(side='right', padx=5)

        # Content area with two panels
        content_frame = tk.Frame(main_frame, bg=DARK_BG)
        content_frame.pack(fill='both', expand=True)

        # Left panel - Thumbnail list
        left_panel = tk.Frame(content_frame, bg='#252525', width=200)
        left_panel.pack(side='left', fill='y', padx=(0, 10))
        left_panel.pack_propagate(False)

        # Thumbnails label
        thumb_label = tk.Label(
            left_panel,
            text="Screenshots",
            font=('Arial', 12, 'bold'),
            fg=LIGHT_TEXT,
            bg='#252525'
        )
        thumb_label.pack(pady=10)

        # Scrollable thumbnail container
        self.thumb_canvas = tk.Canvas(left_panel, bg='#252525', highlightthickness=0)
        thumb_scrollbar = tk.Scrollbar(left_panel, orient='vertical', command=self.thumb_canvas.yview)
        self.thumb_frame = tk.Frame(self.thumb_canvas, bg='#252525')

        self.thumb_frame.bind(
            '<Configure>',
            lambda e: self.thumb_canvas.configure(scrollregion=self.thumb_canvas.bbox('all'))
        )

        self.thumb_canvas.create_window((0, 0), window=self.thumb_frame, anchor='nw')
        self.thumb_canvas.configure(yscrollcommand=thumb_scrollbar.set)

        thumb_scrollbar.pack(side='right', fill='y')
        self.thumb_canvas.pack(side='left', fill='both', expand=True)

        # Right panel - Preview and editing
        right_panel = tk.Frame(content_frame, bg='#252525')
        right_panel.pack(side='right', fill='both', expand=True)

        # Preview image
        self.preview_frame = tk.Frame(right_panel, bg='#1e1e1e')
        self.preview_frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.preview_label = tk.Label(
            self.preview_frame,
            bg='#1e1e1e'
        )
        self.preview_label.pack(expand=True)

        # Editing fields
        edit_frame = tk.Frame(right_panel, bg='#252525', padx=10, pady=10)
        edit_frame.pack(fill='x')

        # Step title
        title_label = tk.Label(
            edit_frame,
            text="Step Title (required):",
            font=('Arial', 11),
            fg=LIGHT_TEXT,
            bg='#252525',
            anchor='w'
        )
        title_label.pack(fill='x', pady=(0, 5))

        self.title_var = tk.StringVar()
        self.title_entry = tk.Entry(
            edit_frame,
            textvariable=self.title_var,
            font=('Arial', 12),
            bg='#1e1e1e',
            fg=LIGHT_TEXT,
            insertbackground=LIGHT_TEXT,
            relief='flat'
        )
        self.title_entry.pack(fill='x', pady=(0, 15), ipady=8)
        self.title_entry.bind('<FocusOut>', lambda e: self.save_current_edits())

        # Notes
        notes_label = tk.Label(
            edit_frame,
            text="Notes (optional):",
            font=('Arial', 11),
            fg=LIGHT_TEXT,
            bg='#252525',
            anchor='w'
        )
        notes_label.pack(fill='x', pady=(0, 5))

        self.notes_text = tk.Text(
            edit_frame,
            font=('Arial', 11),
            bg='#1e1e1e',
            fg=LIGHT_TEXT,
            insertbackground=LIGHT_TEXT,
            relief='flat',
            height=3,
            wrap='word'
        )
        self.notes_text.pack(fill='x', pady=(0, 15))
        self.notes_text.bind('<FocusOut>', lambda e: self.save_current_edits())

        # Alt text
        alt_label = tk.Label(
            edit_frame,
            text="Alt Text (for accessibility):",
            font=('Arial', 11),
            fg=LIGHT_TEXT,
            bg='#252525',
            anchor='w'
        )
        alt_label.pack(fill='x', pady=(0, 5))

        self.alt_text = tk.Text(
            edit_frame,
            font=('Arial', 11),
            bg='#1e1e1e',
            fg=LIGHT_TEXT,
            insertbackground=LIGHT_TEXT,
            relief='flat',
            height=3,
            wrap='word'
        )
        self.alt_text.pack(fill='x', pady=(0, 10))
        self.alt_text.bind('<FocusOut>', lambda e: self.save_current_edits())

        # Navigation buttons
        nav_frame = tk.Frame(edit_frame, bg='#252525')
        nav_frame.pack(fill='x', pady=10)

        self.prev_btn = create_styled_button(
            nav_frame,
            text="< Previous",
            command=self.prev_screenshot,
            font=('Arial', 11),
            padx=15,
            pady=5
        )
        self.prev_btn.pack(side='left')

        self.nav_label = tk.Label(
            nav_frame,
            text="1 of 1",
            font=('Arial', 11),
            fg=MUTED_TEXT,
            bg='#252525'
        )
        self.nav_label.pack(side='left', expand=True)

        self.next_btn = create_styled_button(
            nav_frame,
            text="Next >",
            command=self.next_screenshot,
            font=('Arial', 11),
            padx=15,
            pady=5
        )
        self.next_btn.pack(side='right')

    def load_thumbnails(self):
        """Load thumbnail images for all screenshots"""
        self.thumbnail_images = []
        self.thumb_buttons = []

        for i, ss in enumerate(self.screenshots):
            try:
                img = Image.open(ss['image_path'])
                img.thumbnail((150, 100), Image.Resampling.LANCZOS)
                thumb_img = ImageTk.PhotoImage(img)
                self.thumbnail_images.append(thumb_img)

                # Create thumbnail button
                btn_frame = tk.Frame(self.thumb_frame, bg='#252525', padx=5, pady=5)
                btn_frame.pack(fill='x')

                btn = tk.Button(
                    btn_frame,
                    image=thumb_img,
                    bg='#1e1e1e',
                    activebackground=ACCENT_PURPLE,
                    relief='flat',
                    cursor='hand2',
                    command=lambda idx=i: self.select_screenshot(idx)
                )
                btn.pack()

                step_label = tk.Label(
                    btn_frame,
                    text=f"Step {i + 1}",
                    font=('Arial', 9),
                    fg=MUTED_TEXT,
                    bg='#252525'
                )
                step_label.pack()

                self.thumb_buttons.append((btn_frame, btn))

            except Exception as e:
                print(f"Error loading thumbnail: {e}")

    def select_screenshot(self, index):
        """Select and display a screenshot"""
        if index < 0 or index >= len(self.screenshots):
            return

        # Save current edits first
        self.save_current_edits()

        self.current_index = index
        ss = self.screenshots[index]

        # Update thumbnail selection highlighting
        for i, (frame, btn) in enumerate(self.thumb_buttons):
            if i == index:
                btn.configure(relief='solid', bd=2)
            else:
                btn.configure(relief='flat', bd=0)

        # Load preview image
        try:
            img = Image.open(ss['image_path'])
            # Scale to fit preview area
            max_width = 700
            max_height = 400
            img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            self.preview_image = ImageTk.PhotoImage(img)
            self.preview_label.configure(image=self.preview_image)
        except Exception as e:
            print(f"Error loading preview: {e}")

        # Update editing fields
        self.title_var.set(ss.get('title', f'Step {index + 1}'))

        self.notes_text.delete('1.0', tk.END)
        self.notes_text.insert('1.0', ss.get('notes', ''))

        self.alt_text.delete('1.0', tk.END)
        self.alt_text.insert('1.0', ss.get('alt_text', ''))

        # Update navigation
        self.nav_label.configure(text=f"{index + 1} of {len(self.screenshots)}")

        # Update Previous button state
        if index > 0:
            self.prev_btn.configure(state='normal')
        else:
            self.prev_btn.configure(state='disabled')

        # Update Next button state
        if index < len(self.screenshots) - 1:
            self.next_btn.configure(state='normal')
        else:
            self.next_btn.configure(state='disabled')

    def save_current_edits(self):
        """Save edits to current screenshot"""
        if self.current_index >= len(self.screenshots):
            return

        ss = self.screenshots[self.current_index]
        ss['title'] = self.title_var.get()
        ss['notes'] = self.notes_text.get('1.0', tk.END).strip()
        ss['alt_text'] = self.alt_text.get('1.0', tk.END).strip()

    def prev_screenshot(self):
        """Navigate to previous screenshot"""
        if self.current_index > 0:
            self.select_screenshot(self.current_index - 1)

    def next_screenshot(self):
        """Navigate to next screenshot"""
        if self.current_index < len(self.screenshots) - 1:
            self.select_screenshot(self.current_index + 1)

    def delete_screenshot(self):
        """Delete the current screenshot"""
        if len(self.screenshots) == 0:
            return

        result = messagebox.askyesno(
            "Delete Screenshot",
            f"Are you sure you want to delete Step {self.current_index + 1}?"
        )

        if result:
            # Remove from list
            del self.screenshots[self.current_index]

            if len(self.screenshots) == 0:
                messagebox.showinfo(
                    "No Screenshots",
                    "All screenshots have been deleted."
                )
                self.on_close()
                return

            # Rebuild thumbnails
            for frame, btn in self.thumb_buttons:
                frame.destroy()
            self.load_thumbnails()

            # Select appropriate screenshot
            if self.current_index >= len(self.screenshots):
                self.current_index = len(self.screenshots) - 1
            self.select_screenshot(self.current_index)

    def generate_document(self):
        """Generate the document"""
        # Save current edits
        self.save_current_edits()

        # Validate all screenshots have titles
        missing_titles = []
        for i, ss in enumerate(self.screenshots):
            if not ss.get('title', '').strip():
                missing_titles.append(i + 1)

        if missing_titles:
            messagebox.showwarning(
                "Missing Titles",
                f"Please add titles for steps: {', '.join(map(str, missing_titles))}"
            )
            return

        self.window.destroy()
        self.on_generate(self.screenshots, self.task_name)

    def on_close(self):
        """Handle window close"""
        self.window.destroy()
        self.on_cancel()

