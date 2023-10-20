from fonttoolsWB import App

def test_plugin():
    app = App(test=True)
    assert "fonttools" in app.pluginManager
    assert "output" in app.pluginManager
    assert "shell" in app.pluginManager
    assert "loglist" in app.pluginManager
    assert "uitools" in app.pluginManager
    assert "textedit" in app.pluginManager
    app.Destroy()