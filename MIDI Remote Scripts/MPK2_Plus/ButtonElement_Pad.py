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
		self.color_value = 0
		self.did_change = False		# notifies the MPK2 control surface class that we have a new color we need to send
		self._blink_seq = 0
		self._pulse_seq = 0
		self.blinking = False
		self.pulsing = False

		# set Pad On color for all pads to be black (off) so that user tapping a pad wont make it light up until Ableton tells it to
		# Our realtime color changing will change the Pad Off colors. This is to work around some issues with the MPK2.
		# It seems that if another pads bank is selected other than the one that is having Note On messages sent to it, the pads will light up anyway.
		# Also, when the user lets go of a pad after tapping it, the pad will turn to Off even if Ableton wants it to stay on.
		# So, for our Ableton pad purposes, we will always keep the pads' notes Off and show feedback by changing Pad Off color.
		self.send_midi( (Sysex.SYX_START, ) + (Sysex.SYX_AKAI_ID) + (self._sysex_device_id, ) + (Sysex.SYX_FUNC_SET_PAD_COLOR) + (Sysex.SYX_PAD_ON_BASE_HB, ) + ( Sysex.SYX_PAD_ON_BASE_LB + self._pad_num, ) + (self.color_value, ) + (Sysex.SYX_END, ) )

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
				self.do_pulse(self._pulse_seq)
			# if value is above 16, interpret it as a blinky
			elif (int_color > 16):
				self.blinking = True
				self.pulsing = False
				self.do_blink(self._blink_seq)
			# if neither, it's just a normal color
			else:
				self.blinking = False
				self.pulsing = False
				self.color_value = int_color

			self.did_change = True

	# Pad color changes on the MPK2 for some reason have a delay before applying, unless a pad's note value changes. So we will quickly turn a pad on and off to force a color refresh.
	def send_note_on_off(self):
		super(ButtonElement_Pad, self).send_value(127, False, channel = 9)
		super(ButtonElement_Pad, self).send_value(0, False, channel = 9)

	# called when MPK2 class says it's time to blink
	def do_blink(self, seq):
		self._blink_seq = seq

		if self.blinking == True:
			if seq == 1:
				self.color_value = self._old_value - 17
			else:
				self.color_value = 0
			
			self.did_change = True

	# called when MPK2 class says it's time to pulse. Cycle through predefined pulse color patterns
	def do_pulse(self, seq):
		self._pulse_seq = seq

		if self.pulsing == True:
			if self._old_value - 34 == Colors.GREEN_PULSE[0]:
				self.color_value = Colors.GREEN_PULSE[seq]
			elif self._old_value - 34 == Colors.RED_PULSE[0]:
				self.color_value = Colors.RED_PULSE[seq]

			self.did_change = True
		