# Ara_imgui

**Ara_imgui** is a lightweight and easy-to-use wrapper around [Dear ImGui](https://github.com/ocornut/imgui) using Python and GLFW. It simplifies GUI application development with ImGui by providing a convenient interface for managing windows, fonts, and application lifecycle.

## Features

- Simple ImGui app launch with a single `run` function
- Support for multiple ImGui windows via the `Window` class
- Built-in dark and light themes
- System or custom font loading, including Cyrillic support
- Ready-to-run examples included in the `examples` folder

## Installation

```bash
pip install ara_imgui
````

Or install dependencies manually:

```bash
pip install glfw PyOpenGL imgui ara_core
```

> ⚠️ Make sure you have Python 3.7+ and OpenGL support (e.g., via GPU drivers on Windows).

## Usage

### Basic example

```python
from ara_imgui import run, imgui

app = App("Hello world example")

def gui():
    imgui.text("Hello, world!")
    if imgui.button("Click me"):
        print("Clicked!")

app.run(gui)

```

### Multiple windows

```python
from ara_imgui import App, Window, imgui

app = App("Multi-window App")

def win_gui():
    imgui.text("This is another window")

win = Window("Extra Window", frame_ui=win_gui)

def gui():
    imgui.text("Main Window")  
    if imgui.button("Open Extra Window"):
        app.add_window(win)

app.run(gui)
```

### Custom fonts and themes

```python
from ara_imgui import App, imgui

app = App("Font Example")
app.apply_theme("light")
app.load_font(font_size=18)

def gui():
    imgui.text("Sample text with custom font")

app.run(gui)
```

## Classes

* `App` — The main application class.
* `Window` — Represents a separate ImGui window with its own logic.

## Examples

See the [`examples/`](./examples) folder:

* `hello_world.py` — Basic "Hello, world!" with a button.
* `basic_window.py` — Simple window with input field.
* `custom_font.py` — Font and multilingual text rendering.
* `multiple_window.py` — GUI with multiple ImGui windows.

## Dependencies

* `ara_core`
* `imgui`
* `glfw`
* `PyOpenGL`

## License

MIT License. Free to use and modify.