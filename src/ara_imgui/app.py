import os
import sys
from pathlib import Path
import imgui
from imgui.integrations.glfw import GlfwRenderer  # GLFW integration for ImGui
from ara_core import App as AppCore
from .window import Window

class AraImgui:
    def __init__(self, core):
        self.core = core
        core.add_module(self)
    
    
    def init(self):
        # Initialize ImGui context and GLFW renderer
        imgui.create_context()
        self.renderer = GlfwRenderer(self.core.window)
        
        # ImGui windows set
        self.windows = set()
    
    
    def process_input(self):
        self.renderer.process_inputs()
        
        # Start new ImGui frame
        imgui.new_frame()
        
        
    def render(self):
        pass
        
        
    def update(self):
        # End ImGui frame
        imgui.render()
        self.renderer.render(imgui.get_draw_data())
        
        
    def terminate(self):
        self.renderer.shutdown()
        
        
    # -------- ImGUI management --------
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



class App(AppCore):
    def __init__(self, title="New app", width=800, height=600, log_level="warning"):
        """Initialize the application.
        
        Args:
            title (str): Window title.
            width (int): Window width.
            height (int): Window height.
            log_level (str): Logging level, default is "warning".
        """
        super().__init__(title, width, height, log_level)
        self.ara_imgui = AraImgui(self)
    
    
    def load_font(self, font_path=None, font_size=14, cyrillic_ranges=True):
        """
        Loads a font for the application.

        Args:
            font_path (str, optional): The path to the font file. Defaults to None, which loads the default font.
            font_size (int, optional): The size of the font. Defaults to 14.
            cyrillic_ranges (bool, optional): Whether to include Cyrillic character ranges. Defaults to True.
        """
        
        self.ara_imgui.load_font(font_path, font_size, cyrillic_ranges)
        

    def apply_theme(self, name: str):
        """
        Applies a theme to the application.

        Args:
            name (str): The name of the theme ("dark" or "light").
        """
        self.ara_imgui.apply_theme(name)
        

    def add_window(self, window: Window):
        """
        Adds a window to the application.

        Args:
            window (Window): The Window instance to add.

        Returns:
            bool: True if the window was added, False if it was already present.
        """
        return self.ara_imgui.add_window(window)


    def run(self, frame_ui=None, callback=None, terminate=None):
        """Run the main application loop.
        
        Args:
            frame_ui: Optional UI rendering callback.
            callback: Optional per-frame callback.
            terminate: Optional cleanup callback.
        """
        
        def imgui_ui():
            # Set window size and position
            imgui.set_next_window_position(0, 0)
            imgui.set_next_window_size(self.width, self.height)
            imgui.begin(
                f"##{self.title}", 
                flags=imgui.WINDOW_NO_DECORATION | 
                      imgui.WINDOW_NO_MOVE | 
                      imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS
            )
            
            # Rendering
            frame_ui()
            
            imgui.end()
            
            # Drawing ImGui windows
            self.ara_imgui.windows = set([window for window in self.ara_imgui.windows if not window.should_close])

            for window in self.ara_imgui.windows:
                window.draw()
                
            # End ImGui frame
            imgui.render()
            self.ara_imgui.renderer.render(imgui.get_draw_data())
            

        super().run(imgui_ui, callback, terminate)
            
    
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