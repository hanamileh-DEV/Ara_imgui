import inspect
import imgui

class Window:
    def __init__(self, title, flags=0, frame_ui=None):
        self.name = title
        self.flags = flags
        self.frame_ui = frame_ui
        self.should_close = False
        self._internal_id = id(self)
        self.next_size = None
        self.next_pos = None

    
    def set_frame_ui(self, frame_ui):
        self.frame_ui = frame_ui
    

    def set_size(self, width, height):
        self.next_size = (width, height)


    def set_pos(self, x, y):
        self.next_pos = (x, y)


    def draw(self):
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