from ara_imgui import App, imgui

app = App("Imgui Example", 500, 800)

checkboxs = [True, False, False]
radio_selected = 0
text_input = "Michail"
int_val = 50
float_val = 0.5
combo_selected = 0
color = [1.0, 0.5, 0.0]

def gui():
    global radio_selected, text_input
    global int_val, float_val
    global combo_selected, color
    
    # Text
    imgui.text("This is a text")
    imgui.text("Hello, world!")
    
    # Separator
    imgui.separator()

    # Buttons, same_line and tooltips
    if imgui.button("Button 1"):
        print("Button 1 clicked")
    
    if imgui.is_item_hovered():
        imgui.set_tooltip("This is a tooltip text")
    
    imgui.same_line()
        
    if imgui.button("Button 2"):
        print("Button 2 clicked")
        
    imgui.same_line()
        
    if imgui.button("Button 3"):
        print("Button 3 clicked")
    
    imgui.separator()
    
    # Checkbox
    changed, checkboxs[0] = imgui.checkbox("Checkbox 1", checkboxs[0])
    changed, checkboxs[1] = imgui.checkbox("Checkbox 2", checkboxs[1])
    changed, checkboxs[2] = imgui.checkbox("Checkbox 3", checkboxs[2])

    imgui.separator()
    
    # Radio buttons
    if imgui.radio_button("Radio 1", radio_selected == 0):
        radio_selected = 0
        print("Radio 1 clicked")

    if imgui.radio_button("Radio 2", radio_selected == 1):
        radio_selected = 1
        print("Radio 2 clicked")
        
    if imgui.radio_button("Radio 3", radio_selected == 2):
        radio_selected = 2
        print("Radio 3 clicked")

    imgui.separator()
    
    # Text input
    changed, text_input = imgui.input_text("Text Input", text_input)
    
    imgui.text(f"Hello, {text_input if text_input else "unknown"}!")
    
    imgui.separator()
    
    # Number input
    changed, int_val = imgui.input_int("Int input", int_val)
    changed, float_val = imgui.input_float("Float input", float_val)
    
    imgui.separator()
    
    # Sliders
    changed, int_val = imgui.slider_int("Slider int", int_val, 0, 100)
    changed, float_val = imgui.slider_float("Slider float", float_val, 0.0, 1.0)
    
    imgui.separator()
    
    # Progressbar
    imgui.text("Progress:")
    imgui.progress_bar(float_val)
    
    imgui.separator()
    
    # Combo box
    changed, combo_selected = imgui.combo("Combo", combo_selected, ["Option 1", "Option 2", "Option 3"])
    
    imgui.text(f"Selected option: {combo_selected}")
    
    imgui.separator()
    
    # Color picker
    changed, color = imgui.color_edit3("Color picker", color[0], color[1], color[2])
    
    imgui.separator()
    
    # Child
    if imgui.begin_child("Child", border = True, height = 70):
        imgui.text("This is a child")
        imgui.text("Hello, world!")
        
        for i in range(10):
            imgui.text(f"Child text {i}")
        
        imgui.end_child()
        
    imgui.separator()
    
    # Tree Node
    if imgui.tree_node("Tree node 1"):
        imgui.button("Child 1")
        
        if imgui.tree_node("Child 2"):
            imgui.button("Child 2")
            imgui.button("Child 3")
            imgui.tree_pop()
        
        if imgui.tree_node("Child 3"):
            imgui.button("Child 4")
            imgui.button("Child 5")
            imgui.button("Child 6")
            imgui.tree_pop()

        imgui.tree_pop()

    imgui.separator()
    
    # Table
    if imgui.begin_child("Table", border = True, height = 100):
        imgui.columns(5, "##table columns", border = True)
        
        for i in range(4):
            for j in range(5):
                imgui.text(f"item {i} {j}")
                imgui.next_column()
                
        imgui.columns(1)
        imgui.end_child()


app.run(gui)