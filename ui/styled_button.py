"""
TaskShot Styled Button - Consistent button styling with rounded corners and hover effects
"""

import tkinter as tk

# Brand Colors
PRIMARY_PURPLE = "#a23b84"
HOVER_BLACK = "#000000"
LIGHT_TEXT = "#ffffff"
DISABLED_BG = "#555555"
DISABLED_FG = "#b0b0b0"


class RoundedButton(tk.Canvas):
    """
    A button with rounded corners using Canvas.
    """

    def __init__(self, parent, text, command, font=('Arial', 12, 'bold'),
                 padx=15, pady=8, corner_radius=12, bg=PRIMARY_PURPLE,
                 fg=LIGHT_TEXT, hover_bg=HOVER_BLACK, width=None, **kwargs):

        self.command = command
        self.bg_color = bg
        self.fg_color = fg
        self.hover_bg = hover_bg
        self.corner_radius = corner_radius
        self.text = text
        self.font = font
        self._state = 'normal'

        # Create a temporary label to measure text size
        temp_label = tk.Label(parent, text=text, font=font)
        text_width = temp_label.winfo_reqwidth()
        text_height = temp_label.winfo_reqheight()
        temp_label.destroy()

        # Calculate canvas size
        if width:
            canvas_width = width
        else:
            canvas_width = text_width + (padx * 2)
        canvas_height = text_height + (pady * 2)

        # Initialize canvas
        super().__init__(parent, width=canvas_width, height=canvas_height,
                        bg=parent.cget('bg'), highlightthickness=0, **kwargs)

        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        # Draw the button
        self._draw_button(self.bg_color)

        # Draw the text
        self.text_id = self.create_text(
            canvas_width / 2, canvas_height / 2,
            text=text, font=font, fill=fg
        )

        # Bind events
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        self.bind('<Button-1>', self._on_click)
        self.bind('<ButtonRelease-1>', self._on_release)

        # Change cursor
        self.configure(cursor='hand2')

    def _draw_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        """Draw a rounded rectangle on the canvas."""
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1,
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def _draw_button(self, color):
        """Draw the button background."""
        self.delete('bg')
        self._draw_rounded_rect(
            2, 2, self.canvas_width - 2, self.canvas_height - 2,
            self.corner_radius, fill=color, outline=color, tags='bg'
        )
        # Make sure text stays on top
        if hasattr(self, 'text_id'):
            self.tag_raise(self.text_id)

    def _on_enter(self, event):
        if self._state == 'normal':
            self._draw_button(self.hover_bg)

    def _on_leave(self, event):
        if self._state == 'normal':
            self._draw_button(self.bg_color)

    def _on_click(self, event):
        if self._state == 'normal':
            self._draw_button(self.hover_bg)

    def _on_release(self, event):
        if self._state == 'normal' and self.command:
            self.command()

    def configure(self, **kwargs):
        """Configure button properties."""
        if 'state' in kwargs:
            self._state = kwargs.pop('state')
            if self._state == 'disabled':
                self._draw_button(DISABLED_BG)
                self.itemconfig(self.text_id, fill=DISABLED_FG)
                super().configure(cursor='')
            else:
                self._draw_button(self.bg_color)
                self.itemconfig(self.text_id, fill=self.fg_color)
                super().configure(cursor='hand2')

        if 'bg' in kwargs:
            self.bg_color = kwargs.pop('bg')
            if self._state == 'normal':
                self._draw_button(self.bg_color)

        if 'fg' in kwargs:
            self.fg_color = kwargs.pop('fg')
            if self._state == 'normal':
                self.itemconfig(self.text_id, fill=self.fg_color)

        if 'text' in kwargs:
            self.text = kwargs.pop('text')
            self.itemconfig(self.text_id, text=self.text)

        super().configure(**kwargs)

    # Alias for tkinter compatibility
    config = configure

    def cget(self, key):
        """Get configuration value."""
        if key == 'state':
            return self._state
        elif key == 'bg':
            return self.bg_color
        elif key == 'fg':
            return self.fg_color
        elif key == 'text':
            return self.text
        return super().cget(key)

    def __getitem__(self, key):
        return self.cget(key)


def create_styled_button(parent, text, command, font=('Arial', 12, 'bold'),
                         padx=15, pady=8, width=None, corner_radius=12):
    """
    Create a styled button with rounded corners, purple background and black hover effect.

    Args:
        parent: Parent widget
        text: Button text
        command: Button command callback
        font: Font tuple (family, size, weight)
        padx: Horizontal padding
        pady: Vertical padding
        width: Optional fixed width
        corner_radius: Radius for rounded corners

    Returns:
        Configured RoundedButton widget
    """
    return RoundedButton(
        parent, text=text, command=command, font=font,
        padx=padx, pady=pady, corner_radius=corner_radius,
        bg=PRIMARY_PURPLE, fg=LIGHT_TEXT, hover_bg=HOVER_BLACK,
        width=width
    )


def create_secondary_button(parent, text, command, font=('Arial', 11),
                            padx=15, pady=5, width=None):
    """
    Create a secondary styled button (smaller, same styling).
    """
    return create_styled_button(parent, text, command, font, padx, pady, width)


def apply_hover_to_button(btn, normal_bg=PRIMARY_PURPLE, hover_bg=HOVER_BLACK):
    """
    Apply hover effects to an existing button.
    For RoundedButton, just update the colors.
    For regular buttons, bind hover events.

    Args:
        btn: Existing button widget
        normal_bg: Background color in normal state
        hover_bg: Background color on hover
    """
    if isinstance(btn, RoundedButton):
        btn.bg_color = normal_bg
        btn.hover_bg = hover_bg
        if btn._state == 'normal':
            btn._draw_button(normal_bg)
    else:
        # Regular tk.Button
        def on_enter(e):
            if btn['state'] != 'disabled':
                btn.configure(bg=hover_bg)

        def on_leave(e):
            if btn['state'] != 'disabled':
                btn.configure(bg=normal_bg)

        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
