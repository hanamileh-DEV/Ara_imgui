import imgui

def apply_theme(name: str):
   if name == "dark":
      imgui.style_colors_dark()
   elif name == "light":
      imgui.style_colors_light()
   else:
      raise ValueError(f"Unknown theme name: {name}")