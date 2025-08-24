from ara_imgui import App, imgui

app = App("Hello world example")

def gui():
   imgui.text("Hello, world!")

   if imgui.button("Click me"):
      print("Clicked!")

app.run(gui)
