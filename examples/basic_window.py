from ara_imgui import App, imgui

app = App("Basic Window")

name = ""
def gui():
   global name
   imgui.text("Example of a basic window")

   _, name = imgui.input_text("Enter your name", name)

   imgui.text(f"Hello, {name if len(name) > 0 else "Unknown"}!")


app.run(gui)