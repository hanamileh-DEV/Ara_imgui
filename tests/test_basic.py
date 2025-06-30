# Test if the module can be imported
def test_import():
   import ara_imgui

# Test if the module can be run
def test_run_callable():
   from ara_imgui import run
   assert callable(run)