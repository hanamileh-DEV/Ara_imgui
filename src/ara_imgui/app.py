import os
import sys
from pathlib import Path
import inspect
import glfw
import imgui
from imgui.integrations.glfw import GlfwRenderer  # GLFW integration for ImGui
from .window import Window

class App:
    """
    A class representing an ImGui application.

    Attributes:
        title (str): The title of the application window.
        width (int): The width of the application window.
        height (int): The height of the application window.
        window (GLFWwindow): The GLFW window object.
        renderer (GlfwRenderer): The ImGui GLFW renderer.
        windows (set): A set of Window instances.
    """
    def __init__(self, title="New app", width=800, height=600):
        """
        Initializes the App instance.

        Args:
            title (str, optional): The title of the application window. Defaults to "New app".
            width (int, optional): The width of the application window. Defaults to 800.
            height (int, optional): The height of the application window. Defaults to 600.
        """
        # Initialize GLFW
        if not glfw.init():
            raise Exception("Failed to initialize GLFW")
        
        # Set window properties
        self.title = title
        self.width = width
        self.height = height
        
        # Create GLFW window
        self.window = glfw.create_window(width, height, title, None, None)

        if not self.window:
            glfw.terminate()
            raise Exception("Failed to create GLFW window")
        
        # Set up OpenGL context and vsync
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)  # Enable vsync
        
        # Initialize ImGui context and GLFW renderer
        imgui.create_context()
        self.renderer = GlfwRenderer(self.window)
        
        # ImGui windows
        self.windows = set()

    
    def load_font(self, font_path=None, font_size=14, cyrillic_ranges=True):
        """
        Loads a font for the application.

        Args:
            font_path (str, optional): The path to the font file. Defaults to None, which loads the default font.
            font_size (int, optional): The size of the font. Defaults to 14.
            cyrillic_ranges (bool, optional): Whether to include Cyrillic character ranges. Defaults to True.
        """
        # Loading default font
        if font_path is None:
            if sys.platform == "win32":
                font_path = Path("C:/Windows/Fonts/segoeui.ttf")
            elif sys.platform == "darwin":
                font_path = Path("/System/Library/Fonts/SFNSDisplay.ttf")
            elif sys.platform == "linux":
                font_path = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
            else:
                raise Exception(f"Unsupported platform {sys.platform}")

        # Check if font file exists
        if not os.path.exists(font_path):
            raise Exception(f"Font file {font_path} does not exist")

        # Loading font
        io = imgui.get_io()

        glyph_ranges = io.fonts.get_glyph_ranges_default()

        if cyrillic_ranges:
            glyph_ranges = io.fonts.get_glyph_ranges_cyrillic()

        io.fonts.clear()
        io.fonts.add_font_from_file_ttf(str(font_path), font_size, None, glyph_ranges)
        self.renderer.refresh_font_texture()


    def apply_theme(self, name: str):
        """
        Applies a theme to the application.

        Args:
            name (str): The name of the theme ("dark" or "light").
        """
        if name == "dark":
            imgui.style_colors_dark()
        elif name == "light":
            imgui.style_colors_light()
        else:
            raise ValueError(f"Unknown theme name: {name}. Available themes: 'dark', 'light'")


    def add_window(self, window: Window):
        """
        Adds a window to the application.

        Args:
            window (Window): The Window instance to add.

        Returns:
            bool: True if the window was added, False if it was already present.
        """
        window.should_close = False
        if window not in self.windows:
            self.windows.add(window)
            return True
        else:
            return False


    def run(self, frame_ui = None, callback = None):
        """
        Executes the main application loop.

        Args:
            frame_ui (function, optional): The function to draw the main UI. Defaults to None.
            callback (function, optional): The function to call after drawing the UI. Defaults to None.
        """

        while not glfw.window_should_close(self.window):
            # Process events and inputs
            glfw.poll_events()
            self.renderer.process_inputs()
            
            # Start new ImGui frame
            imgui.new_frame()

            # Get current window size
            self.width, self.height = glfw.get_framebuffer_size(self.window)

            # Set up fullscreen window for ImGui main window
            imgui.set_next_window_position(0, 0)
            imgui.set_next_window_size(self.width, self.height)
            imgui.begin(
                f"##{self.title}", 
                flags=imgui.WINDOW_NO_DECORATION | 
                      imgui.WINDOW_NO_MOVE | 
                      imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS
            )
            
            # Call UI rendering callback if set
            if frame_ui:
                sig = inspect.signature(frame_ui)
                if len(sig.parameters) == 0:
                    frame_ui()
                elif len(sig.parameters) == 1:
                    frame_ui(self)
                else:
                    raise TypeError(f"frame_ui function must take 0 or 1 arguments, but {len(sig.parameters)} were given")
            
            imgui.end()

            # Drawing ImGui windows
            self.windows = set([window for window in self.windows if not window.should_close])

            for window in self.windows:
                window.draw()

            # Call frame update callback if set
            if callback:
                sig = inspect.signature(callback)
                if len(sig.parameters) == 0:
                    callback()
                elif len(sig.parameters) == 1:
                    callback(self)
                else:
                    raise TypeError(f"callback function must take 0 or 1 arguments, but {len(sig.parameters)} were given")

            # Render ImGui and swap buffers
            imgui.render()
            self.renderer.render(imgui.get_draw_data())
            glfw.swap_buffers(self.window)

        # Cleanup on exit
        self.renderer.shutdown()
        glfw.terminate()

    
def run(
        frame_ui,
        callback=None,
        title="New app",
        width=800,
        height=600,
        theme="dark",
        custom_font=False,
        font_size=14,
        cyrillic_ranges=True
    ):
    """
    A minimalistic, easy-to-use function for creating and running an app.

    Args:
        frame_ui (function): The function to draw the main UI.
        callback (function, optional): The function to call after drawing the UI. Defaults to None.
        title (str, optional): The title of the application window. Defaults to "New app".
        width (int, optional): The width of the application window. Defaults to 800.
        height (int, optional): The height of the application window. Defaults to 600.
        theme (str, optional): The name of the theme ("dark" or "light"). Defaults to "dark".
        custom_font (bool or str, optional): The path to a custom font or True to use the default font or False to use build-in ImGui font. Defaults to False.
        font_size (int, optional): The size of the font. Defaults to 14.
        cyrillic_ranges (bool, optional): Whether to include Cyrillic character ranges. Defaults to True.
    """

    app = App(title, width, height)

    if custom_font == True:
        app.load_font(font_size=font_size, cyrillic_ranges=cyrillic_ranges)
    elif type(custom_font) == str:
        app.load_font(font_path=custom_font, font_size=font_size, cyrillic_ranges=cyrillic_ranges)

    app.apply_theme(theme)
    app.run(frame_ui, callback)