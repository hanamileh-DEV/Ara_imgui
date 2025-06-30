from ara_imgui import run, imgui

def gui():
   imgui.text("Hello, world!")

   if imgui.button("Click me"):
      print("Clicked!")

run(gui)
