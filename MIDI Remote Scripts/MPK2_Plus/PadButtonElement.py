#
#   PadButtonElement.py
#   Derived ButtonElement class that stores this pad's index, so its Color can send the sysex message to set the right pad's color.
#

from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ButtonElement import ButtonElement, DummyUndoStepHandler
from .Skin import Skin
from . import Sysex

class PadButtonElement(ButtonElement):

    def __init__(self, is_momentary, msg_type, channel, identifier, pad_num = 0, skin = Skin(), undo_step_handler = DummyUndoStepHandler(), *a, **k):
        super(PadButtonElement, self).__init__(is_momentary, msg_type, channel, identifier, skin, undo_step_handler, *a, **k)
        self._pad_num = pad_num

    # override send_value function (called by either Color class or ClipSlotComponent) to send sysex message to change the pad color too
    def send_value(self, value, force = False, channel = None):
        if (value != 0):
            self.send_midi( (Sysex.SYX_START) + Sysex.SYX_AKAI_ID + (Sysex.SYX_DEVICE_ID_MPK249) + Sysex.SYX_FUNC_SET_PAD_COLOR + (Sysex.SYX_PAD_ON_BASE + self._pad_num) + (value) + (Sysex.SYX_END) )
            super(PadButtonElement, self).send_value(self, 127, force, channel)
        else:
            super(PadButtonElement, self).send_value(self, 0, force, channel)
