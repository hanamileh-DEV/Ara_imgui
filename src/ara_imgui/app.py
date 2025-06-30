import os
import sys
from pathlib import Path
import glfw
import imgui
from imgui.integrations.glfw import GlfwRenderer  # GLFW integration for ImGui
from .theme import apply_theme

class App:
    def __init__(self, title="New app", width=800, height=600):
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

        # Callbacks for frame updates and UI rendering
        self.frame_callback = None  # Called each frame for app logic
        self.frame_ui = None        # Called each frame for UI rendering

    
    def set_frame_callback(self, callback):
        """Set the callback function for frame updates"""
        self.frame_callback = callback

    
    def set_frame_ui(self, ui):
        """Set the callback function for UI rendering"""
        self.frame_ui = ui

    
    def load_font(self, font_path=None, font_size=14, cyrillic_ranges=False):
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


    def run(self):
        """Executing the main application loop"""
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
            if self.frame_ui:
                self.frame_ui()
            
            imgui.end()

            # Call frame update callback if set
            if self.frame_callback:
                self.frame_callback()

            # Render ImGui and swap buffers
            imgui.render()
            self.renderer.render(imgui.get_draw_data())
            glfw.swap_buffers(self.window)

        # Cleanup on exit
        self.renderer.shutdown()
        glfw.terminate()

    
def run(frame_ui, frame_callback=None, title="New app", width=800, height=600, theme="dark"):
    """A minimalistic, easy-to-use function for creating and running an app"""
    app = App(title, width, height)
    apply_theme(theme)
    app.set_frame_ui(frame_ui)
    app.set_frame_callback(frame_callback)
    app.run()