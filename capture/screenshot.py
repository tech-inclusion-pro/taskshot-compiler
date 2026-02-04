"""
TaskShot Screenshot Capture - Screen capture with cursor overlay
"""

import platform
import subprocess
import tempfile
import time
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw

# Try to import mss for cross-platform screenshots
try:
    import mss
    HAS_MSS = True
except ImportError:
    HAS_MSS = False

# Try to import pygame for audio feedback
try:
    import pygame
    pygame.mixer.init()
    HAS_PYGAME = True
except ImportError:
    HAS_PYGAME = False


class ScreenshotCapture:
    """Handles screenshot capture with cursor position overlay"""

    def __init__(self, settings):
        self.settings = settings
        self.system = platform.system()
        self.screenshot_dir = Path(tempfile.gettempdir()) / "taskshot_screenshots"
        self.screenshot_dir.mkdir(exist_ok=True)
        self.screenshot_count = 0
        self.last_capture_time = 0
        self.min_capture_interval = 0.3  # Minimum 300ms between captures

        # Load click sound if available
        self.click_sound = None
        if HAS_PYGAME:
            sound_path = Path(__file__).parent.parent / "assets" / "sounds" / "click.wav"
            if sound_path.exists():
                try:
                    self.click_sound = pygame.mixer.Sound(str(sound_path))
                except Exception:
                    pass

    def capture(self, x, y):
        """
        Capture a screenshot and add cursor position indicator.

        Args:
            x: Mouse x coordinate
            y: Mouse y coordinate

        Returns:
            dict with screenshot data or None on failure
        """
        # Debounce: prevent captures that are too close together
        current_time = time.time()
        if current_time - self.last_capture_time < self.min_capture_interval:
            return None
        self.last_capture_time = current_time

        # Play audio feedback
        if self.settings.get('sound_feedback', True) and self.click_sound:
            try:
                self.click_sound.play()
            except Exception:
                pass

        # Capture screenshot
        image = self._capture_screen()
        if image is None:
            print(f"Failed to capture screen at ({x}, {y})")
            return None

        # Add cursor position circle
        image = self._add_cursor_circle(image, x, y)

        # Save screenshot
        self.screenshot_count += 1
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{self.screenshot_count:03d}_{timestamp}.png"
        filepath = self.screenshot_dir / filename

        try:
            image.save(str(filepath), "PNG")
        except Exception as e:
            print(f"Error saving screenshot: {e}")
            return None

        return {
            'image_path': str(filepath),
            'timestamp': datetime.now().isoformat(),
            'x': x,
            'y': y,
            'step_number': self.screenshot_count,
            'title': '',
            'notes': '',
            'alt_text': f"Screenshot {self.screenshot_count} - Step in tutorial"
        }

    def _capture_screen(self):
        """Capture the full screen"""
        try:
            # On macOS, prefer native screencapture for reliability
            if self.system == "Darwin":
                return self._capture_macos()
            elif HAS_MSS:
                return self._capture_with_mss()
            elif self.system == "Windows":
                return self._capture_windows()
            elif self.system == "Linux":
                return self._capture_linux()
            else:
                print(f"Unsupported platform: {self.system}")
                return None
        except Exception as e:
            print(f"Screenshot capture error: {e}")
            return None

    def _capture_with_mss(self):
        """Capture screen using mss library"""
        try:
            with mss.mss() as sct:
                # Capture primary monitor (index 1 is main display, index 0 is all monitors combined)
                # Use monitor[1] for primary display to get proper full screen capture
                if len(sct.monitors) > 1:
                    monitor = sct.monitors[1]  # Primary monitor
                else:
                    monitor = sct.monitors[0]  # Fallback to all monitors
                screenshot = sct.grab(monitor)
                # Convert to PIL Image
                img = Image.frombytes('RGB', screenshot.size, screenshot.bgra, 'raw', 'BGRX')
                return img
        except Exception as e:
            print(f"mss capture error: {e}")
            return None

    def _capture_macos(self):
        """Capture full screen on macOS using screencapture"""
        temp_file = self.screenshot_dir / f"temp_capture_{time.time()}.png"

        # Try mss first as it's more reliable for repeated captures
        if HAS_MSS:
            try:
                result = self._capture_with_mss()
                if result is not None:
                    return result
            except Exception as e:
                print(f"mss capture failed: {e}, trying screencapture...")

        # Fallback to native screencapture
        try:
            # -x: no sound, -C: capture cursor (captures all screens by default)
            result = subprocess.run(
                ["screencapture", "-x", str(temp_file)],
                check=True,
                capture_output=True,
                timeout=10
            )

            if not temp_file.exists():
                print("Screenshot file was not created")
                return None

            image = Image.open(str(temp_file))
            image.load()  # Force load before deleting temp file
            try:
                temp_file.unlink()
            except Exception:
                pass  # Ignore cleanup errors
            return image
        except subprocess.CalledProcessError as e:
            print(f"screencapture failed: {e.stderr.decode() if e.stderr else e}")
            return None
        except subprocess.TimeoutExpired:
            print("screencapture timed out")
            return None
        except FileNotFoundError:
            print("screencapture command not found")
            return None
        except Exception as e:
            print(f"macOS screenshot error: {e}")
            return None

    def _capture_windows(self):
        """Capture screen on Windows"""
        try:
            from PIL import ImageGrab
            return ImageGrab.grab()
        except Exception as e:
            print(f"Windows screenshot failed: {e}")
            return None

    def _capture_linux(self):
        """Capture screen on Linux using scrot or gnome-screenshot"""
        temp_file = self.screenshot_dir / f"temp_capture_{time.time()}.png"

        # Try scrot first
        try:
            subprocess.run(
                ["scrot", str(temp_file)],
                check=True,
                capture_output=True
            )
            image = Image.open(str(temp_file))
            image.load()
            temp_file.unlink()
            return image
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

        # Try gnome-screenshot
        try:
            subprocess.run(
                ["gnome-screenshot", "-f", str(temp_file)],
                check=True,
                capture_output=True
            )
            image = Image.open(str(temp_file))
            image.load()
            temp_file.unlink()
            return image
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

        print("No screenshot tool available (tried scrot, gnome-screenshot)")
        return None

    def _add_cursor_circle(self, image, x, y):
        """
        Add a circle overlay at the cursor position.

        Args:
            image: PIL Image object
            x: Cursor x coordinate
            y: Cursor y coordinate

        Returns:
            Modified PIL Image with circle overlay
        """
        # Get settings
        color = self.settings.get('circle_color', '#FF0000')
        size = self.settings.get('circle_size', 40)
        line_width = 3

        # Create drawing context
        draw = ImageDraw.Draw(image)

        # Calculate circle bounds
        radius = size // 2
        x0 = x - radius
        y0 = y - radius
        x1 = x + radius
        y1 = y + radius

        # Draw circle outline (no fill)
        draw.ellipse(
            [x0, y0, x1, y1],
            outline=color,
            width=line_width
        )

        return image

    def cleanup(self):
        """Clean up temporary screenshot files"""
        try:
            for file in self.screenshot_dir.glob("*.png"):
                file.unlink()
        except Exception as e:
            print(f"Cleanup error: {e}")
