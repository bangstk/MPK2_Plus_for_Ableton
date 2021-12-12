#
#   MPK249_Plus.py
#   Main controller code for MPK249
#

from __future__ import absolute_import, print_function, unicode_literals
import Live
from _Framework.ControlSurface import ControlSurface, MIDI_CC_TYPE, MIDI_NOTE_TYPE
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.SessionComponent import SessionComponent
from MPK2_Plus.PadButtonElement import PadButtonElement
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

PADS_WIDTH = 4
PADS_HEIGHT = 4

class MPK249_Plus(ControlSurface):

    def __init__(self, *a, **k):
        super(MPK249_Plus, self).__init__(*a, **k)

        with self.component_guard():
            self._create_controls()
            self._create_session()

    def _create_controls(self):
        # Nav
        self._btn_nav_up = ButtonElement(True, msg_type = MIDI_CC_TYPE, channel = 1, identifier = CC_NAV, name = u'Nav_Up_Button')
        self._btn_nav_down = ButtonElement(True, msg_type = MIDI_CC_TYPE, channel = 1, identifier = CC_NAV + 1, name = u'Nav_Down_Button')
        self._btn_nav_left = ButtonElement(True, msg_type = MIDI_CC_TYPE, channel = 1, identifier = CC_NAV + 2, name = u'Nav_Left_Button')
        self._btn_nav_right = ButtonElement(True, msg_type = MIDI_CC_TYPE, channel = 1, identifier = CC_NAV + 3, name = u'Nav_Right_Button')
        self._btn_nav_ok = ButtonElement(True, msg_type = MIDI_CC_TYPE, channel = 1, identifier = CC_NAV + 4, name = u'Nav_OK_Button')

        # Pads
        pad_rows = ()
        current_pad_num = 0
        for i in range(PADS_HEIGHT):
            pad_row = ()
            for j in range(PADS_WIDTH):
                current_pad_num += 1
                pad_row += PadButtonElement(True, msg_type = MIDI_NOTE_TYPE, channel = 9, identifier = NOTE_PADS + current_pad_num, pad_num = current_pad_num, name = 'Pad_{}_{}'.format(j, i))
            pad_rows.insert(0, pad_row) # put new row before the previous one, because the MPK2 numbers the pads starting from bottom and not top
        self._btn_pads_matrix = ButtonMatrixElement(rows = pad_rows, name=u'Pad_Button_Matrix')
    
    def _create_session(self):
        self._session = SessionComponent(num_tracks = PADS_WIDTH, num_scenes = PADS_WIDTH, name = u'Session', is_enabled = False, enable_skinning = True)
        self._session.set_scene_bank_buttons(down_button = self._btn_nav_down, up_button = self._btn_nav_up_button)
        self._session.set_track_bank_buttons(right_button = self._btn_nav_right, left_button = self._btn_nav_left)
        self._session.set_clip_launch_buttons(self._btn_pads_matrix)
        self._session.set_rgb_mode(color_palette = LIVE_RGB_VALUE_TO_MIDI_VALUE_TABLE, color_table = MIDI_VALUE_TO_RGB_COLOR_TABLE)
        self._session.set_show_highlight(show_highlight = 1)
        self._session.set_enabled(True)