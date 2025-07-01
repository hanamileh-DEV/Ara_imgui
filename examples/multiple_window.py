from ara_imgui import App, Window, imgui

# First ImGui window
def gui_1():
    imgui.text("Hello from Window 1")
    imgui.button("Button")

win_1 = Window("Window 1", frame_ui=gui_1)
win_1.set_pos(50, 50)
win_1.set_size(300, 250)


# Second ImGui window
def gui_2(window):
    imgui.text("Hello from Window 2")
    _, window.val = imgui.slider_int("Slider", window.val, 0, 100)

win_2 = Window("Window 2", frame_ui=gui_2)
win_2.set_pos(80, 60)
win_2.val = 50


# Main window
app = App("Multiple Window")

def gui_main():
    imgui.text("Hello from Main Window")

    if imgui.button("Open Window 1"):
        app.add_window(win_1)

    if imgui.button("Open Window 2"):
        app.add_window(win_2)


app.run(gui_main)