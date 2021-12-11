#
#   PadButtonElement.py
#   Derived ButtonElement class that stores this pad's index, so its Color can send the sysex message to set the right pad's color.
#

from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ButtonElement import ButtonElement

class PadButtonElement(ButtonElement):

    def __init__(self, is_momentary, msg_type, channel, identifier, pad_num = 0, skin = Skin(), undo_step_handler = DummyUndoStepHandler(), *a, **k):
        super(PadButtonElement, self).__init__(msg_type, channel, identifier, skin, undo_step_handler, *a, **k)
        self._pad_num = pad_num

    def _set_skin_light(self, value):
        try:
            color = self._skin[value]
            color.draw(self, self._pad_num)
        except SkinColorMissingError:
            super(PadButtonElement, self).set_light(value)