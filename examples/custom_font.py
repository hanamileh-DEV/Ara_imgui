from ara_imgui import App, imgui, apply_theme

app = App("Custom font example")

def gui():
   imgui.text("Latin characters:")
   imgui.text("The quick brown fox jumps over the lazy dog")
   imgui.text("Cyrillic characters:")
   imgui.text("Съешь ещё этих мягких французкий булок да выпей же чаю")

   imgui.separator()
   imgui.text("Text example:")
   imgui.text("Lorem ipsum dolor sit amet consectetur adipiscing")
   imgui.text("elit, sed do eiusmod tempor incididunt ut labore")
   imgui.text("et dolore magna aliqua. Ut enim ad minim veniam,")
   imgui.text("quis nostrud exercitation ullamco laboris nisi ut")
   imgui.text("aliquip ex ea commodo consequat. Duis aute irure")
   imgui.text("dolor in reprehenderit in voluptate velit esse")
   imgui.text("cillum dolore eu fugiat nulla pariatur.")


app.apply_theme("light")
app.load_font(font_size=20, cyrillic_ranges=True)
app.run(gui)