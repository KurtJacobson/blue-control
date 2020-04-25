from qtpyvcp.widgets.qtdesigner import _DesignerPlugin

from my_line_edit import MyLineEdit
class MyLineEditPlugin(_DesignerPlugin):
    def pluginClass(self):
        return MyLineEdit
