from ara_imgui import App, imgui

app = App("Basic Window", log_level="info")

name = ""
def gui():
   global name
   imgui.text("Example of a basic window")

   changed, name = imgui.input_text("Enter your name", name)

   if changed:
      print(f"Input text: {name}")

   imgui.text(f"Hello, {name if name else "Unknown"}!")
   
   io = imgui.get_io()
   
   imgui.text(f"Keys down: {sum(io.keys_down)}")
   
   if app.core.key_down("w"):
      print("w is pressed!")


app.run(gui)