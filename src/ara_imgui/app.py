import os
import sys
from pathlib import Path
import glfw
import imgui
from imgui.integrations.glfw import GlfwRenderer  # GLFW integration for ImGui
from ara_core import App as AppCore
from .window import Window

class AraImgui:
    NAME="ara_imgui"
    DEPENDENCIES = {
        "new_frame": {
            "before": ["core.render", "core.update"],
            "after": []
        },
        "finish_frame": {
            "before": [],
            "after": ["core.render"]
        }
    }
    
    
    def __init__(self, core):
        self.core = core
        core.add_module(self)
    
    
    def init(self):
        # Initialize ImGui context and GLFW renderer
        imgui.create_context()
        self.renderer = GlfwRenderer(self.core.window, attach_callbacks=False)
        
        # ImGui windows set
        self.windows = set()
        
        # Changing GLFW custom callbacks
        glfw.set_key_callback(self.core.window, self._key_callback)
        glfw.set_char_callback(self.core.window, self._char_callback)
        glfw.set_scroll_callback(self.core.window, self._scroll_callback)
    
    
    def _key_callback(self, window, key, scancode, action, mods):
        io = imgui.get_io()
        
        if io.want_capture_keyboard:
            self.renderer.keyboard_callback(window, key, scancode, action, mods)
        
        self.core._key_callback(window, key, scancode, action, mods)
        
    
    def _char_callback(self, window, char):
        io = imgui.get_io()

        if io.want_capture_keyboard:
            self.renderer.char_callback(window, char)
            
        # (Core doesn't have custom char callback)


    def _scroll_callback(self, window, xpos, ypos):
        io = imgui.get_io()

        if io.want_capture_mouse:
            self.renderer.scroll_callback(window, xpos, ypos)

        self.core._scroll_callback(window, xpos, ypos)

    
    def terminate(self):
        self.renderer.shutdown()
        
        
    # ========= Mode callbacks =========
    def new_frame(self):
        self.renderer.process_inputs()
        imgui.new_frame()
        
        
    def finish_frame(self):
        imgui.render()
        self.renderer.render(imgui.get_draw_data())
    
        
    # ========= ImGUI utitities =========
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


class App():
    def __init__(self, title="New app", width=800, height=600, log_level="warning"):
        """Initialize the application.
        
        Args:
            title (str): Window title.
            width (int): Window width.
            height (int): Window height.
            log_level (str): Logging level, default is "warning".
        """
        core = AppCore(title, width, height, log_level)
        
        self.core = core
        self.ara_imgui = AraImgui(core)
        
        # core.add_module(self.ara_imgui)
        
    
    
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


    def run(self, render=None, update=None, terminate=None):
        """Run main loop with dependency-resolved callbacks
        
        Args:
            render (function, optional): Render callback. Defaults to None.
            update (function, optional): Update callback. Defaults to None.
            terminate (function, optional): Terminate callback. Defaults to None.
        """
            
        def imgui_render():
            # Set window size and position
            imgui.set_next_window_position(0, 0)
            imgui.set_next_window_size(self.core.width, self.core.height)
            imgui.begin(
                f"##{self.core.title}", 
                flags=imgui.WINDOW_NO_DECORATION | 
                      imgui.WINDOW_NO_MOVE | 
                      imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS
            )
            
            # Rendering
            render()
            
            imgui.end()
            
            # Drawing ImGui windows
            self.ara_imgui.windows = set([window for window in self.ara_imgui.windows if not window.should_close])

            for window in self.ara_imgui.windows:
                window.draw()
                
            # End ImGui frame
            imgui.render()
            self.ara_imgui.renderer.render(imgui.get_draw_data())
            

        self.core.run(imgui_render, update, terminate)