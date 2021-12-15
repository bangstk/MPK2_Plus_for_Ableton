#
#	MPK249_Plus.py
#	Main controller code for MPK249
#

from __future__ import absolute_import, print_function, unicode_literals
import Live
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ControlSurface import ControlSurface, MIDI_CC_TYPE, MIDI_NOTE_TYPE
from _Framework.DrumGroupComponent import DrumGroupComponent
from _Framework.EncoderElement import EncoderElement
from _Framework.MixerComponent import MixerComponent
from _Framework import Task
from _Framework.TransportComponent import TransportComponent
from _Framework.Util import const
from _Framework.SessionComponent import SessionComponent
from _Framework.SliderElement import SliderElement
from MPK2_Plus.ButtonElement_Pad import ButtonElement_Pad
from MPK2_Plus.Colors import LIVE_RGB_VALUE_TO_MIDI_VALUE_TABLE, MIDI_VALUE_TO_RGB_COLOR_TABLE
from MPK2_Plus.DeviceComponent_MultiBank import DeviceComponent_MultiBank
from MPK2_Plus.Skin import make_default_skin
from MPK2_Plus import Sysex

# hardware and layout definitions
SYX_DEVICE_ID = 0x24

PADS_WIDTH = 4
PADS_HEIGHT = 4

NUM_MIXER_BANKS = 3
NUM_MIXER_TRAX = 8

BLINK_WAIT_TIME_SECS = 1 / 8

# MIDi note/CC definitions - based on MPK2's Bitwig preset
CC_NAV = 60
CC_TRANSPORT = 114
CC_KNOBS = 50
CC_FADERS = 40
CC_BUTTONS = 30
NOTE_PADS = 36

class MPK249_Plus(ControlSurface):

	# define sysex device id here so MPK261 can inherit this class & override the id
	sysex_device_id = SYX_DEVICE_ID

	def __init__(self, *a, **k):
		super(MPK249_Plus, self).__init__(*a, **k)
		
		self._skin = make_default_skin()
		
		with self.component_guard():
			self._create_controls()
			self._create_transport()
			self._create_device()
			self.set_device_component(self._device)
			self._create_mixer()
			self._create_session()
			self.set_highlighting_session_component(self._session)
			# self._create_drums()

		# set up looping tasks to deal with pad colors
		# Two of the tasks run as fast as possible because Task.wait() seems to have a minimum time that is too long for a smooth refresh rate.
		# Ableton doesn't seem to make that a busy loop, CPU usage is not affected by not having a wait. So it's fine I guess.
		# We have code later that makes sure we only send a pads color update only when needed, instead of at every tick.
		#
		# TODO: match pad blink/pulse time to current tempo
		self._blink_seq = 0
		self._pulse_seq = 0
		self._task_pad_color = self._tasks.add(Task.loop( Task.run(self._send_all_pad_colors) ) )
		self._task_pad_blink = self._tasks.add(Task.loop( Task.sequence(Task.run(self._send_pad_blink), Task.wait(BLINK_WAIT_TIME_SECS) ) ) )
		self._task_pad_pulse = self._tasks.add(Task.loop( Task.run(self._send_pad_pulse) ) )

	# Create objects for all physical controls
	def _create_controls(self):
		# Nav
		self._btn_nav_up = ButtonElement(is_momentary = True, msg_type = MIDI_CC_TYPE, channel = 1, identifier = CC_NAV, name = u'Button_Nav_Up')
		self._btn_nav_down = ButtonElement(is_momentary = True, msg_type = MIDI_CC_TYPE, channel = 1, identifier = CC_NAV + 1, name = u'Button_Nav_Down')
		self._btn_nav_left = ButtonElement(is_momentary = True, msg_type = MIDI_CC_TYPE, channel = 1, identifier = CC_NAV + 2, name = u'Button_Nav_Left')
		self._btn_nav_right = ButtonElement(is_momentary = True, msg_type = MIDI_CC_TYPE, channel = 1, identifier = CC_NAV + 3, name = u'Button_Nav_Right')
		self._btn_nav_ok = ButtonElement(is_momentary = True, msg_type = MIDI_CC_TYPE, channel = 1, identifier = CC_NAV + 4, name = u'Button_Nav_Ok')

		# Transport
		self._btn_tp_loop = ButtonElement(is_momentary = False, msg_type = MIDI_CC_TYPE, channel = 0, identifier = CC_TRANSPORT, name = u'Button_Transport_Loop')
		self._btn_tp_rw = ButtonElement(is_momentary = False, msg_type = MIDI_CC_TYPE, channel = 0, identifier = CC_TRANSPORT + 1, name = u'Button_Transport_Rewind')
		self._btn_tp_ff = ButtonElement(is_momentary = False, msg_type = MIDI_CC_TYPE, channel = 0, identifier = CC_TRANSPORT + 2, name = u'Button_Transport_Fastforward')
		self._btn_tp_stop = ButtonElement(is_momentary = False, msg_type = MIDI_CC_TYPE, channel = 0, identifier = CC_TRANSPORT + 3, name = u'Button_Transport_Stop')
		self._btn_tp_play = ButtonElement(is_momentary = False, msg_type = MIDI_CC_TYPE, channel = 0, identifier = CC_TRANSPORT + 4, name = u'Button_Transport_Play')
		self._btn_tp_rec = ButtonElement(is_momentary = False, msg_type = MIDI_CC_TYPE, channel = 0, identifier = CC_TRANSPORT + 5, name = u'Button_Transport_Record')

		# Knobs
		knobs_list = []
		for i in range (NUM_MIXER_BANKS):
			for j in range (NUM_MIXER_TRAX):
				new_knob = EncoderElement(msg_type = MIDI_CC_TYPE, channel = i + 1, identifier = CC_KNOBS + j, map_mode = Live.MidiMap.MapMode.relative_smooth_two_compliment, name = u'Knob_{}'.format(i * NUM_MIXER_TRAX + j))
				new_knob.mapping_sensitivity = 2.0	# make knob movement speed match what is seen on Ableton's macro knob - easier to go from 0 to max value with 1 twist of wrist too
				knobs_list.append(new_knob)
		self._knobs_matrix = ButtonMatrixElement(rows = [knobs_list])

		# Faders
		faders_list = []
		for i in range (NUM_MIXER_BANKS):
			for j in range (NUM_MIXER_TRAX):
				new_fader = SliderElement(msg_type = MIDI_CC_TYPE, channel = i + 1, identifier = CC_FADERS + j, name = u'Fader_{}'.format(i * NUM_MIXER_TRAX + j))
				faders_list.append(new_fader)
		self._faders_matrix = ButtonMatrixElement(rows = [faders_list])

		# Buttons
		buttons_list = []
		for i in range (NUM_MIXER_BANKS):
			for j in range (NUM_MIXER_TRAX):
				new_btn = ButtonElement(is_momentary = True, msg_type = MIDI_CC_TYPE, channel = i + 1, identifier = CC_BUTTONS + j, name = u'Button_Mixer_{}'.format(i * NUM_MIXER_TRAX + j))
				buttons_list.append(new_btn)
		self._btns_matrix = ButtonMatrixElement(rows = [buttons_list])

		# Pads Bank A (Session)
		pad_rows_bank_a = []
		current_pad_num = 0
		for i in range(PADS_HEIGHT):
			pad_row = []
			for j in range(PADS_WIDTH):
				pad_button = ButtonElement_Pad(is_momentary = True, msg_type = MIDI_NOTE_TYPE, channel = 9, identifier = NOTE_PADS + current_pad_num, pad_num = current_pad_num, sysex_device_id = self.sysex_device_id, skin = self._skin, name = u'Pad_A_{}_{}'.format(j, i) )
				current_pad_num = current_pad_num + 1
				pad_row.append( pad_button )
			pad_rows_bank_a.insert(0, pad_row) # put new row before the previous one, because the MPK2 numbers the pads starting from bottom and not top
		self._btn_pads_bank_a_matrix = ButtonMatrixElement(rows = pad_rows_bank_a, name = u'Pad_Button_Matrix')
		
		# Pads Bank D (Drums)
		pad_rows_bank_d = []
		current_pad_num = 0
		for i in range(PADS_HEIGHT):
			pad_row = []
			for j in range(PADS_WIDTH):
				pad_button = ButtonElement_Pad(True, msg_type = MIDI_NOTE_TYPE, channel = 9, identifier = NOTE_PADS + 48 + current_pad_num, pad_num = 48 + current_pad_num, sysex_device_id = self.sysex_device_id, skin = self._skin, name = u'Pad_D_{}_{}'.format(j, i) )
				current_pad_num = current_pad_num + 1
				pad_row.append( pad_button )
			pad_rows_bank_d.insert(0, pad_row) # put new row before the previous one, because the MPK2 numbers the pads starting from bottom and not top
		self._btn_pads_bank_d_matrix = ButtonMatrixElement(rows = pad_rows_bank_d, name = u'Drum_Pad_Button_Matrix')
	
	# Assign knobs to device component
	def _create_device(self):
		self._device = DeviceComponent_MultiBank(device_selection_follows_track_selection = True, name = u'Device', is_enabled = False)
		self._device.set_parameter_controls(self._knobs_matrix)
		self._device.set_enabled(True)

	# Assign transport buttons to transport component
	def _create_transport(self):
		self._transport = TransportComponent(name = u'Transport', is_enabled = False)
		self._transport.set_seek_buttons(self._btn_tp_ff, self._btn_tp_rw)
		self._transport.set_play_button(self._btn_tp_play)
		self._transport.set_stop_button(self._btn_tp_stop)
		self._transport.set_record_button(self._btn_tp_rec)
		self._transport.set_loop_button(self._btn_tp_loop)
		self._transport.set_enabled(True)

	# Assign faders and mixer buttons to mixer component
	def _create_mixer(self):
		self._mixer = MixerComponent(num_tracks = NUM_MIXER_BANKS * NUM_MIXER_TRAX, name = u'Mixer', is_enabled = False)
		self._mixer.set_volume_controls(self._faders_matrix)
		self._mixer.set_arm_buttons(self._btns_matrix)
		self._mixer.set_enabled(True)

	# Assign pad buttons and nav buttons to session component
	def _create_session(self):
		self._session = SessionComponent(num_tracks = PADS_WIDTH, num_scenes = PADS_WIDTH, name = u'Session', is_enabled = False, enable_skinning = True)
		self._session.set_scene_bank_buttons(down_button = self._btn_nav_down, up_button = self._btn_nav_up)
		self._session.set_track_bank_buttons(right_button = self._btn_nav_right, left_button = self._btn_nav_left)
		self._session.set_clip_launch_buttons(self._btn_pads_bank_a_matrix)
		self._session.set_rgb_mode(color_palette = LIVE_RGB_VALUE_TO_MIDI_VALUE_TABLE, color_table = MIDI_VALUE_TO_RGB_COLOR_TABLE)
		self._session.set_show_highlight(True)
		self._session.set_enabled(True)
	
	# Assign pad buttons to drums component
	def _create_drums(self):
		self._drums = DrumGroupComponent(translation_channel = 9, name = u'Drums', is_enabled = False)
		self._drums.set_drum_matrix(self._btn_pads_bank_d_matrix)
		self._drums.set_enabled(True)
	
	# Polls all pads for its color index, sends a sysex message to MPK2 to update all pads colors at once
	def _send_all_pad_colors(self):
		pad_colors = ()
		pad_row = ()
		pad = None

		pad_row_count = 0
		something_changed = False

		# check if a pad changed since last send, if so, gather all pad colors into a list and send it thru sysex
		for pad in self._btn_pads_bank_a_matrix:
			if pad.did_change == True:
				something_changed = True

			# MPK2 pad button order starts from the bottom row, so we have to stuff each new row at the beginning of the color list
			pad_row += (pad.color_value, )
			pad.did_change = False
			pad_row_count += 1

			if pad_row_count == PADS_WIDTH:
				pad_row_count = 0
				pad_colors = pad_row + pad_colors
				pad_row = ()

		# doesnt matter what button object we send from, so just use the last one
		# We are using Pad Off colors for our Ableton session. See ButtonElement_Pad for details.
		if something_changed == True:
			pad.send_midi( (Sysex.SYX_START, ) + Sysex.SYX_AKAI_ID + (self.sysex_device_id, ) + Sysex.SYX_FUNC_SET_PAD_COLOR_ALL + (Sysex.SYX_PAD_OFF_BASE_HB, ) + ( Sysex.SYX_PAD_OFF_BASE_LB, ) + pad_colors + (Sysex.SYX_END, ) )
			pad.send_note_on_off()	# pad color changes seem to be delayed until a pad note event happens, so always do one

	# tell all pads to blink. Each pad will decide if it needs to blink or ignore this. We call them from here so all pads will blink in sync at any time.
	def _send_pad_blink(self):
		for pad in self._btn_pads_bank_a_matrix:
			pad.do_blink(self._blink_seq)

		if (self._blink_seq == 0):
			self._blink_seq = 1
		else:
			self._blink_seq = 0

	# tell all pads to go to the next color in the Pulsing color sequence. Each pad will decide if it needs to pulse or ignore this.
	def _send_pad_pulse(self):
		seq = self._pulse_seq

		for pad in self._btn_pads_bank_a_matrix:
			pad.do_pulse(seq)
			
		self._pulse_seq += 1

		if self._pulse_seq > 5:
			self._pulse_seq = 0
