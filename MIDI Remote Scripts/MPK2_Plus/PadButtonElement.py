#
#	PadButtonElement.py
#	Derived ButtonElement class that stores this pad's index, so the button can also send the sysex message to set the correct pad's color.
#

from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ButtonElement import ButtonElement, DummyUndoStepHandler
from .Skin import Skin
from . import Sysex

# Button used for pads only that sends sysex messages for color changing
class PadButtonElement(ButtonElement):

	def __init__(self, is_momentary, msg_type, channel, identifier, pad_num = 0, sysex_device_id = 0x24, skin = Skin(), undo_step_handler = DummyUndoStepHandler(), *a, **k):
		super(PadButtonElement, self).__init__(is_momentary, msg_type, channel, identifier, skin, undo_step_handler, *a, **k)
		self._pad_num = pad_num
		self._sysex_device_id = sysex_device_id
		self._old_value = -1
		# set Pad On color for all pads to be black (off) so that user tapping a pad wont make it light up until Ableton tells it to
		self.send_midi( (Sysex.SYX_START, ) + (Sysex.SYX_AKAI_ID) + (self._sysex_device_id, ) + (Sysex.SYX_FUNC_SET_PAD_COLOR) + (Sysex.SYX_PAD_ON_BASE_HB, ) + ( Sysex.SYX_PAD_ON_BASE_LB + self._pad_num, ) + (0, ) + (Sysex.SYX_END, ) )

	# override send_value function (called by either Color class or ClipSlotComponent) to send sysex message to change the pad color.
	# TODO: Merge all pad color sysex messages into 1 single message to set all pads
	# This would cut down on the MIDI traffic considerably
	def send_value(self, value, force = False, channel = None): 

		int_value = int(value)

		if (int_value != self._old_value):      # don't fill up the MIDI bus if the color hasn't changed
			self._old_value = int_value

			# Pad color changing is accomplished by writing to the MPK's memory using Sysex messages.
			# For the 'Pad Off' colors, there is a gap in the memory after the first 4 pads.
			# This is due to Sysex messages not being allowed to contain a byte greater than 7F.
			# So we have to check if the address would be '0x0A80' and if so skipping to '0x0B00'
			pad_off_hb = Sysex.SYX_PAD_OFF_BASE_HB
			pad_off_lb = Sysex.SYX_PAD_OFF_BASE_LB
			temp_pad_num = self._pad_num 
			
			if (temp_pad_num < 4):
				pad_off_lb += temp_pad_num
			else:
				pad_off_hb += 1
				pad_off_lb = temp_pad_num - 4

			if (int_value != 0):
				# Set Pad Off as the color and send Note Off - if we use Pad On color, the pad will turn off when user lets go of pad until Ableton sends the next message
				self.send_midi( (Sysex.SYX_START, ) + (Sysex.SYX_AKAI_ID) + (self._sysex_device_id, ) + (Sysex.SYX_FUNC_SET_PAD_COLOR) + (pad_off_hb, ) + ( pad_off_lb, ) + (int_value, ) + (Sysex.SYX_END, ) )
				super(ButtonElement, self).send_value(0, force, channel)
			elif (int_value == 0):
				# for some reason, using Note On for blank clips is much less laggy on the MPK2 pads.
				self.send_midi( (Sysex.SYX_START, ) + (Sysex.SYX_AKAI_ID) + (self._sysex_device_id, ) + (Sysex.SYX_FUNC_SET_PAD_COLOR) + (pad_off_hb, ) + ( pad_off_lb, ) + (0, ) + (Sysex.SYX_END, ) )
				super(ButtonElement, self).send_value(127, force, channel)