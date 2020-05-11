"""DRO Line Entry"""
import os
import linuxcnc

from qtpy.QtWidgets import QLineEdit
from qtpy.QtCore import Slot, Property

from qtpyvcp.plugins import getPlugin
from qtpyvcp.widgets import CMDWidget
from qtpyvcp.utilities import logger

STATUS = getPlugin('status')
POSITION = getPlugin('position')

LOG = logger.getLogger(__name__)

INIFILE = linuxcnc.ini(os.getenv("INI_FILE_NAME"))
IN_DESIGNER = os.getenv('DESIGNER') != None


class DROEntry(QLineEdit, CMDWidget):

    def __init__(self, parent=None):
        super(DROEntry, self).__init__(parent)

        self._settings = {}

    @Property(str)
    def settings(self):
        return str(self._settings)

    @settings.setter
    def settings(self, settings):
        self._settings = settings
