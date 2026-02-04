"""
TaskShot Mouse Listener - Global mouse event capture
"""

import threading
import platform

# Try to import pynput for global mouse listening
try:
    from pynput import mouse
    HAS_PYNPUT = True
except ImportError:
    HAS_PYNPUT = False


class MouseListener:
    """
    Global mouse listener that captures clicks even when app is not in focus.
    Uses pynput for cross-platform compatibility.
    """

    def __init__(self, on_click, settings):
        """
        Initialize the mouse listener.

        Args:
            on_click: Callback function(x, y, button) called on each click
            settings: Settings object for configuration
        """
        self.on_click_callback = on_click
        self.settings = settings
        self.listener = None
        self.running = False
        self._restart_count = 0
        self._max_restarts = 10

        if not HAS_PYNPUT:
            print("Warning: pynput not installed. Mouse listening may not work.")
            print("Install with: pip install pynput")

    def _create_listener(self):
        """Create a new mouse listener instance"""
        def on_click(x, y, button, pressed):
            """Handle mouse click event"""
            if not self.running:
                return False

            # Only capture on mouse down (pressed=True)
            if pressed:
                # Determine button type
                button_type = "left"
                if button == mouse.Button.right:
                    button_type = "right"
                elif button == mouse.Button.middle:
                    button_type = "middle"

                # Call the callback
                try:
                    self.on_click_callback(int(x), int(y), button_type)
                except Exception as e:
                    print(f"Click handler error: {e}")
                    # Don't let exceptions stop the listener

            return self.running  # Keep listening while running

        return mouse.Listener(on_click=on_click)

    def start(self):
        """Start listening for mouse clicks"""
        if not HAS_PYNPUT:
            return

        self.running = True
        self._restart_count = 0
        self._start_listener()

    def _start_listener(self):
        """Internal method to start/restart the listener"""
        if not self.running:
            return

        # Clean up old listener if exists
        if self.listener:
            try:
                self.listener.stop()
            except Exception:
                pass

        # Create and start new listener
        self.listener = self._create_listener()
        self.listener.start()

        # Start a watchdog thread to ensure listener stays alive
        watchdog = threading.Thread(target=self._watchdog, daemon=True)
        watchdog.start()

    def _watchdog(self):
        """Monitor the listener and restart if it dies unexpectedly"""
        import time
        while self.running:
            time.sleep(0.5)
            if self.running and self.listener and not self.listener.is_alive():
                if self._restart_count < self._max_restarts:
                    self._restart_count += 1
                    print(f"Mouse listener died, restarting (attempt {self._restart_count})")
                    self._start_listener()
                    return  # New watchdog will be started by _start_listener
                else:
                    print("Max restart attempts reached for mouse listener")

    def stop(self):
        """Stop listening for mouse clicks"""
        self.running = False

        if self.listener:
            try:
                self.listener.stop()
            except Exception:
                pass
            self.listener = None


class KeyboardShortcutListener:
    """
    Global keyboard listener for shortcuts.
    Uses pynput for cross-platform compatibility.
    """

    def __init__(self, callbacks):
        """
        Initialize the keyboard listener.

        Args:
            callbacks: Dict of shortcut -> callback function
                       e.g., {'start': func, 'stop': func, 'help': func}
        """
        self.callbacks = callbacks
        self.listener = None
        self.running = False
        self.current_keys = set()

        # Platform-specific modifier key
        self.system = platform.system()
        self.ctrl_key = 'cmd' if self.system == 'Darwin' else 'ctrl'

    def start(self):
        """Start listening for keyboard shortcuts"""
        if not HAS_PYNPUT:
            return

        from pynput import keyboard

        self.running = True

        def on_press(key):
            """Handle key press"""
            if not self.running:
                return False

            # Track current keys
            try:
                key_name = key.char if hasattr(key, 'char') else key.name
            except AttributeError:
                return True

            self.current_keys.add(key_name)

            # Check for shortcuts (Ctrl/Cmd + Shift + key)
            has_ctrl = 'ctrl_l' in self.current_keys or 'ctrl_r' in self.current_keys
            has_cmd = 'cmd' in self.current_keys or 'cmd_r' in self.current_keys
            has_shift = 'shift' in self.current_keys or 'shift_r' in self.current_keys

            modifier = has_cmd if self.system == 'Darwin' else has_ctrl

            if modifier and has_shift:
                if key_name == 's' and 'start' in self.callbacks:
                    self.callbacks['start']()
                elif key_name == 'x' and 'stop' in self.callbacks:
                    self.callbacks['stop']()
                elif key_name == 'h' and 'help' in self.callbacks:
                    self.callbacks['help']()
                elif key_name == 'e' and 'settings' in self.callbacks:
                    self.callbacks['settings']()

            return True

        def on_release(key):
            """Handle key release"""
            try:
                key_name = key.char if hasattr(key, 'char') else key.name
                self.current_keys.discard(key_name)
            except AttributeError:
                pass
            return True

        # Create and start the listener
        self.listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        self.listener.start()

    def stop(self):
        """Stop listening for keyboard shortcuts"""
        self.running = False

        if self.listener:
            try:
                self.listener.stop()
            except Exception:
                pass
            self.listener = None
