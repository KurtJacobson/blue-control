from qtpyvcp.widgets.qtdesigner import _DesignerPlugin

from my_line_edit import MyLineEdit
class MyLineEdit_Plugin(_DesignerPlugin):
    def pluginClass(self):
        return MyLineEdit

from my_push_button import MyPushButton
class MyPushButton_Plugin(_DesignerPlugin):
    def pluginClass(self):
        return MyPushButton
