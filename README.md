<p align="center">
  <img src="assets/icons/taskshot_icon.png" alt="TaskShot Logo" width="200"/>
</p>

<h1 align="center">TaskShot</h1>

<p align="center">
  <strong>Accessible Screenshot Documentation Tool</strong><br>
  Create step-by-step tutorials with automatic screenshot capture
</p>

<p align="center">
  Made by <a href="https://github.com/Tech-Inclusion-Pro">Rocco Catrone of Tech Inclusion Pro</a><br>
  Licensed under MIT License - Free and Open Source
</p>

---

## What is TaskShot?

TaskShot is an open-source, accessible screenshot documentation tool designed with **Universal Design for Learning (UDL)** and **WCAG 2.1 AA compliance** at its core. It allows you to capture screenshots by simply clicking through your workflow, then generates accessible Word documents perfect for tutorials, training materials, and documentation.

### Key Features

- **Click-to-Capture**: Every mouse click captures a screenshot automatically
- **Visual Click Indicator**: Red circle shows exactly where you clicked
- **Step-by-Step Review**: Review, title, and add notes to each screenshot
- **Alt Text Support**: Add accessibility descriptions to every image
- **Accessible Output**: Generates WCAG 2.1 AA compliant Word documents
- **Full Keyboard Navigation**: Complete keyboard accessibility
- **Screen Reader Compatible**: Works with assistive technologies
- **Customizable Settings**: Adjust colors, sizes, and feedback options

---

## Installation

### Prerequisites

- **Python 3.10 or higher**
- **pip** (Python package manager)

### Step 1: Clone the Repository

```bash
git clone https://github.com/Tech-Inclusion-Pro/TaskShot-Compiler.git
cd TaskShot-Compiler
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run TaskShot

```bash
python3 main.py
```

---

## Platform-Specific Instructions

### macOS

#### Required Permissions

TaskShot needs the following permissions to capture screenshots and detect mouse clicks:

1. **Screen Recording Permission**
   - Go to **System Settings** → **Privacy & Security** → **Screen Recording**
   - Click **+** and add **Terminal** (or your terminal app)
   - Restart TaskShot after granting permission

2. **Accessibility / Input Monitoring Permission**
   - Go to **System Settings** → **Privacy & Security** → **Accessibility**
   - Click **+** and add **Terminal** (or your terminal app)
   - You may also need to add it to **Input Monitoring**

#### Creating a macOS App (Optional)

To run TaskShot from your Applications folder:

1. Create the app bundle structure:
```bash
mkdir -p /Applications/TaskShot.app/Contents/MacOS
mkdir -p /Applications/TaskShot.app/Contents/Resources
```

2. Create the launcher script at `/Applications/TaskShot.app/Contents/MacOS/TaskShot`:
```bash
#!/bin/bash
osascript <<EOF
tell application "Terminal"
    activate
    do script "cd ~/TaskShot && python3 main.py; exit"
end tell
EOF
```

3. Make it executable and sign:
```bash
chmod +x /Applications/TaskShot.app/Contents/MacOS/TaskShot
codesign --force --deep --sign - /Applications/TaskShot.app
```

> **Important Note**: When running from the Applications folder, a **Terminal window will open** - this is normal and required for the app to have proper input monitoring permissions. The Terminal window will close automatically when you quit TaskShot.

---

### Windows

#### Installation

1. Install Python from [python.org](https://www.python.org/downloads/)
   - **Important**: Check "Add Python to PATH" during installation

2. Open Command Prompt or PowerShell and run:
```cmd
git clone https://github.com/Tech-Inclusion-Pro/TaskShot-Compiler.git
cd TaskShot-Compiler
pip install -r requirements.txt
python main.py
```

#### Required Permissions

- Windows may prompt you to allow Python through the firewall
- No special permissions are typically required for screen capture on Windows

#### Creating a Windows Shortcut (Optional)

1. Right-click on your Desktop → **New** → **Shortcut**
2. Enter the location: `pythonw.exe "C:\path\to\TaskShot-Compiler\main.py"`
3. Name it "TaskShot"

---

### Linux

#### Installation

1. Install Python and required system packages:

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-tk scrot
```

**Fedora:**
```bash
sudo dnf install python3 python3-pip python3-tkinter scrot
```

**Arch Linux:**
```bash
sudo pacman -S python python-pip tk scrot
```

2. Clone and install:
```bash
git clone https://github.com/Tech-Inclusion-Pro/TaskShot-Compiler.git
cd TaskShot-Compiler
pip3 install -r requirements.txt
python3 main.py
```

#### Required Permissions

- On Wayland, you may need to use XWayland or grant additional permissions
- Some distributions may require adding your user to the `input` group:
```bash
sudo usermod -a -G input $USER
```
Then log out and back in.

---

## How to Use TaskShot

### Quick Start Guide

1. **Launch TaskShot**
   ```bash
   cd TaskShot-Compiler
   python3 main.py
   ```

2. **Enter a Task Name**
   - Type a descriptive name for your tutorial (e.g., "How to Create a New Document")
   - This will be used as the document filename

3. **Start Capturing**
   - Click **"Start Capture"** or press `Ctrl+Shift+S` (Mac: `Cmd+Shift+S`)
   - The app will minimize to a control bar at the top of your screen

4. **Click Through Your Process**
   - Every mouse click captures a screenshot
   - A red circle indicates where you clicked
   - The counter shows how many screenshots you've captured

5. **Stop Capturing**
   - Click **"Stop Capture"** or press `Ctrl+Shift+X` (Mac: `Cmd+Shift+X`)

6. **Review Your Screenshots**
   - Add a **title** for each step (required)
   - Add optional **notes** for additional context
   - Add **alt text** for accessibility (describes the image for screen readers)

7. **Generate Document**
   - Click **"Generate Document"**
   - Your accessible Word document will be created and saved to your Desktop

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Shift+S` (Mac: `Cmd+Shift+S`) | Start capture |
| `Ctrl+Shift+X` (Mac: `Cmd+Shift+X`) | Stop capture |
| `Ctrl+Shift+H` (Mac: `Cmd+Shift+H`) | Show help |
| `Ctrl+Shift+E` (Mac: `Cmd+Shift+E`) | Open settings |
| `←` `→` Arrow keys | Navigate screenshots in review |
| `Delete` | Remove selected screenshot |

---

## Settings

Access settings by clicking the **Settings** button in the control bar.

### Capture Settings
- **Sound feedback**: Play a sound when capturing
- **Visual flash**: Flash the screen when capturing
- **Circle color**: Color of the click indicator
- **Circle size**: Size of the click indicator (20-80 pixels)

### Document Settings
- **Header color**: Color of section headers in the document
- **Table border color**: Color of borders around images
- **Include footer**: Add accessibility statement to document
- **Margin size**: Document margins (0.5", 0.75", or 1")

---

## Troubleshooting

### "Screen capture not working"
- **macOS**: Grant Screen Recording permission in System Settings → Privacy & Security
- **Linux**: Install `scrot` or `gnome-screenshot`
- **Windows**: Run as Administrator if issues persist

### "Mouse clicks not detected"
- **macOS**: Grant Accessibility and Input Monitoring permissions to Terminal
- **Linux**: Add user to `input` group and re-login
- **All platforms**: Make sure `pynput` is installed: `pip install pynput`

### "App only captures 2 screenshots then stops" (macOS)
- This is a permissions issue. Make sure Terminal has **Input Monitoring** permission
- Run TaskShot from Terminal directly: `cd ~/TaskShot && python3 main.py`

### "Module not found" errors
```bash
pip install -r requirements.txt
```

---

## Dependencies

TaskShot uses the following Python packages:

- `Pillow` - Image processing
- `pynput` - Global mouse/keyboard listening
- `python-docx` - Word document generation
- `mss` - Fast cross-platform screenshots

Install all dependencies:
```bash
pip install -r requirements.txt
```

---

## Output

Documents are saved to your Desktop with the naming format:
```
[TaskName].TaskShot.[YYYY-MM-DD].docx
```

The generated documents include:
- Proper heading structure (H1, H2)
- Table header markup for accessibility
- Alt text for all images
- Language metadata
- Page numbers
- Accessibility footer statement

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Built with accessibility in mind following WCAG 2.1 AA guidelines
- Designed using Universal Design for Learning (UDL) principles
- Created to make documentation accessible to everyone

---

<p align="center">
  Made with care by <strong>Rocco Catrone of Tech Inclusion Pro</strong>
</p>
