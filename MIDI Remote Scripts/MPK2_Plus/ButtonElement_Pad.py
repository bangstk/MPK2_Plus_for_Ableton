#
#	ButtonElement_Pad.py
#	Derived ButtonElement class that stores this pad's index, so the button can also send the sysex message to set the correct pad's color.
#

from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ButtonElement import ButtonElement, DummyUndoStepHandler
from _Framework import Task
from .Skin import Skin
from . import Colors
from . import Sysex

# Button used for pads only that sends sysex messages for color changing
class ButtonElement_Pad(ButtonElement):

	def __init__(self, is_momentary, msg_type, channel, identifier, pad_num = 0, sysex_device_id = 0x24, skin = Skin(), undo_step_handler = DummyUndoStepHandler(), *a, **k):
		super(ButtonElement_Pad, self).__init__(is_momentary, msg_type, channel, identifier, skin, undo_step_handler, *a, **k)
		self._pad_num = pad_num
		self._sysex_device_id = sysex_device_id
		self._old_value = -1
		self._color_value = 0
		self.did_change = False
		self.blinking = False
		self.pulsing = False

		# set Pad On color for all pads to be black (off) so that user tapping a pad wont make it light up until Ableton tells it to
		self.send_midi( (Sysex.SYX_START, ) + (Sysex.SYX_AKAI_ID) + (self._sysex_device_id, ) + (Sysex.SYX_FUNC_SET_PAD_COLOR) + (Sysex.SYX_PAD_ON_BASE_HB, ) + ( Sysex.SYX_PAD_ON_BASE_LB + self._pad_num, ) + (self._color_value, ) + (Sysex.SYX_END, ) )

	# override send_value function (called by either Color class or ClipSlotComponent) to store current pad color. Color is later retrieved & sent by the MPK2 main object's task.
	def send_value(self, value, force = False, channel = None): 
		int_color = int(value)

		# don't fill up the MIDI bus if the color hasn't changed
		if (int_color != self._old_value):
			self._old_value = int_color

			# if value is above 33, interpret it as a pulse
			if (int_color > 33):
				self.pulsing = True
				self.blinking = False
				self._color_value = int_color - 34
			# if value is above 16, interpret it as a blinky
			elif (int_color > 16):
				self.blinking = True
				self.pulsing = False
				self._color_value = int_color - 17
			# if neither, it's just a normal color
			else:
				self.blinking = False
				self.pulsing = False
				self._color_value = int_color

			self.did_change = True

	def get_color(self):
		return self._color_value

	def send_note_on_off(self):
		super(ButtonElement_Pad, self).send_value(127, False, channel = 9)
		super(ButtonElement_Pad, self).send_value(0, False, channel = 9)

	def do_blink_on(self):
		if self.blinking == True:
			self._color_value = self._old_value - 17
			self.did_change = True
	
	def do_blink_off(self):
		if self.blinking == True:
			self._color_value = 0
			self.did_change = True

	def do_pulse(self, seq):
		if self.pulsing == True:
			if self._old_value - 34 == GREEN_PULSE[0]:
				self._color_value = GREEN_PULSE[seq]
			elif self._old_value - 34 == RED_PULSE[0]:
				self._color_value = RED_PULSE[seq]

			self.did_change = True
		