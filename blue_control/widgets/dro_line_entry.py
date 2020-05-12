"""DRO Line Entry"""
import os
import linuxcnc

from qtpy.QtWidgets import QLineEdit
from qtpy.QtCore import Slot, Property

from qtpyvcp.plugins import getPlugin
from qtpyvcp.widgets import CMDWidget
from qtpyvcp.utilities import logger
from qtpyvcp.actions.machine_actions import issue_mdi

STATUS = getPlugin('status')
POSITION = getPlugin('position')

LOG = logger.getLogger(__name__)

INIFILE = linuxcnc.ini(os.getenv("INI_FILE_NAME"))
IN_DESIGNER = os.getenv('DESIGNER') != None


class Axis(object):
    ALL = -1
    X, Y, Z, A, B, C, U, V, W = range(9)


class Units(object):
    Program = 0  # Use program units
    Inch = 1     # CANON_UNITS_INCHES=1
    Metric = 2   # CANON_UNITS_MM=2


class RefType(object):
    Absolute = 0
    Relative = 1
    DistanceToGo = 2

    @classmethod
    def toString(self, ref_type):
        return ['abs', 'rel', 'dtg'][ref_type]


class DROEntry(QLineEdit, CMDWidget):

    def __init__(self, parent=None):
        super(DROEntry, self).__init__(parent)

        self._anum = 0
        self._ref_typ = 0
        self._mm_fmt = '%10.3f'
        self._in_fmt = '%9.4f'

        self._fmt = self._in_fmt

        self.updateValue()

        self.returnPressed.connect(self.onReturnPressed)
        self.editingFinished.connect(self.onEditingFinished)

        issue_mdi.bindOk(widget=self)
        STATUS.program_units.notify(self.updateUnits, 'string')

    def updateUnits(self, units=None):
        if units is None:
            units = str(STATUS.program_units)

        if units == 'in':
            self._fmt = self._in_fmt
        else:
            self._fmt = self._mm_fmt

        # force update
        self.updateValue()

    def onReturnPressed(self):
        try:
            val = float(self.text().strip().replace('mm', '').replace('in', ''))
            g5x_index = STATUS.stat.g5x_index
            axis = 'XYZABCUVW'[self._anum]

            cmd = 'G10 L20 P{0:d} {1}{2:.12f}'.format(g5x_index, axis, val)
            issue_mdi(cmd)
        except Exception:
            LOG.exception("Error setting work coordinate offset.")

        self.blockSignals(True)
        self.clearFocus()
        self.blockSignals(False)

    def onEditingFinished(self):
        self.updateValue()

    def initialize(self):
        getattr(POSITION, RefType.toString(self._ref_typ)).notify(self.updateValue)
        self.updateValue()

    def updateValue(self, pos=None):
        """Refresh displayed text, used in designer."""
        if pos is None:
            pos = getattr(POSITION, RefType.toString(self._ref_typ)).getValue()
        self.setText(self._fmt % pos[self._anum])

    @Property(int)
    def referenceType(self):
        return self._ref_typ

    @referenceType.setter
    def referenceType(self, ref_type):
        self._ref_typ = ref_type
        self.updateValue()

    @Property(int)
    def axisNumber(self):
        return self._anum

    @axisNumber.setter
    def axisNumber(self, axis):
        self._anum = axis
        self.updateValue()

    @Property(str)
    def inchFormat(self):
        return self._in_fmt

    @inchFormat.setter
    def inchFormat(self, inch_format):
        self._in_fmt = inch_format
        self.updateUnits()

    @Property(str)
    def metricFormat(self):
        return self._mm_fmt

    @metricFormat.setter
    def metricFormat(self, metric_format):
        self._mm_fmt = metric_format
        self.updateUnits()
