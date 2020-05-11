from qtpyvcp.widgets.qtdesigner import _DesignerPlugin

from my_line_edit import MyLineEdit
class MyLineEdit_Plugin(_DesignerPlugin):
    def pluginClass(self):
        return MyLineEdit

from my_push_button import MyPushButton
class MyPushButton_Plugin(_DesignerPlugin):
    def pluginClass(self):
        return MyPushButton

from dro_line_entry import DROEntry
from qtdesigner.dro_editor import DroEditorExtension
class DROEntry_Plugin(_DesignerPlugin):
    def pluginClass(self):
        return DROEntry
    def designerExtensions(self):
        return [DroEditorExtension,]
