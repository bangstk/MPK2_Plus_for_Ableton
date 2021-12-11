from __future__ import absolute_import, print_function, unicode_literals
import Live
from _Framework.ControlSurface import ControlSurface
from MPK2_Plus.Colors import LIVE_RGB_VALUE_TO_MIDI_VALUE_TABLE, MIDI_VALUE_TO_RGB_COLOR_TABLE
from MPK2_Plus.Skin import make_default_skin
from MPK2_Plus import Sysex

SYX_DEVICE_ID = 0x24

# CC/note assignments in 'Bitwig' MPK2 preset has everything the way I need.
CC_NAV = 60
CC_TRANSPORT = 114
CC_KNOBS = 50
CC_FADERS = 40
CC_BUTTONS = 30
NOTE_PADS = 36

class MPK249_Plus(ControlSurface):

    def __init__(self, *a, **k):
        super(MPK249_Plus, self).__init__(*a, **k)
