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