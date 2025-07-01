import inspect
import imgui

class Window:
    """
    A class representing an ImGui window.

    Attributes:
        name (str): The title of the window.
        flags (int): The flags for the window.
        frame_ui (function): The function to draw the window's content.
        should_close (bool): A flag indicating if the window should be closed.
        _internal_id (int): The unique ID for the window.
        next_size (tuple, None): The next size of the window.
        next_pos (tuple, None): The next position of the window.
    """
    def __init__(self, title, flags=0, frame_ui=None):
        """
        Initializes the Window instance.

        Args:
            title (str): The title of the window.
            flags (int, optional): The ImGui flags for the window. Defaults to 0.
            frame_ui (function, optional): The function to draw the window's content. Defaults to None.
        """
        self.name = title
        self.flags = flags
        self.frame_ui = frame_ui
        self.should_close = False
        self._internal_id = id(self)
        self.next_size = None
        self.next_pos = None

    
    def set_frame_ui(self, frame_ui):
        """
        Sets the frame UI function for the window.

        Args:
            frame_ui (function): The function to draw the window's content.
        """
        self.frame_ui = frame_ui
    

    def set_size(self, width: int, height: int):
        """
        Sets the size of the window.

        Args:
            width (int): The width of the window.
            height (int): The height of the window.
        """
        self.next_size = (width, height)


    def set_pos(self, x, y):
        """
        Sets the position of the window.

        Args:
            x (int): The x-coordinate of the window.
            y (int): The y-coordinate of the window.
        """
        self.next_pos = (x, y)


    def draw(self):
        """
        Draws the window and its content.

        This method sets the size and position of the window if they have been changed,
        begins the ImGui window, and calls the frame UI function if it exists.
        """
        if self.next_size:
            imgui.set_next_window_size(self.next_size[0], self.next_size[1])
            self.next_size = None

        if self.next_pos:
            imgui.set_next_window_position(self.next_pos[0], self.next_pos[1])
            self.next_pos = None

        _, is_opened = imgui.begin(f"{self.name}##{self._internal_id}", True, flags = self.flags)

        self.should_close = not is_opened

        if self.frame_ui is not None:
            sig = inspect.signature(self.frame_ui)
            if len(sig.parameters) == 0:
                self.frame_ui()
            elif len(sig.parameters) == 1:
                self.frame_ui(self)
            else:
                raise TypeError(f"frame_ui function must take 0 or 1 arguments, but {len(sig.parameters)} were given")

        imgui.end()