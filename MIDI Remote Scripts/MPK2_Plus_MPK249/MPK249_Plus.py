#
#	MPK249_Plus.py
#	Main controller code for MPK249
#

from __future__ import absolute_import, print_function, unicode_literals
import Live
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ControlSurface import ControlSurface, MIDI_CC_TYPE, MIDI_NOTE_TYPE
from _Framework.DeviceComponent import DeviceComponent
from _Framework.DrumGroupComponent import DrumGroupComponent
from _Framework.EncoderElement import EncoderElement
from _Framework.MixerComponent import MixerComponent
from _Framework.TransportComponent import TransportComponent
from _Framework.Util import const
from _Framework.SessionComponent import SessionComponent
from _Framework.SliderElement import SliderElement
from MPK2_Plus.PadButtonElement import PadButtonElement
from MPK2_Plus.Colors import LIVE_RGB_VALUE_TO_MIDI_VALUE_TABLE, MIDI_VALUE_TO_RGB_COLOR_TABLE
from MPK2_Plus.Skin import make_default_skin
from MPK2_Plus import Sysex

# hardware and layout definitions
SYX_DEVICE_ID = 0x24

PADS_WIDTH = 4
PADS_HEIGHT = 4

NUM_MIXER_BANKS = 3
NUM_MIXER_TRAX = 8

# MIDi note/CC definitions - based on MPK2's Bitwig preset
CC_NAV = 60
CC_TRANSPORT = 114
CC_KNOBS = 50
CC_FADERS = 40
CC_BUTTONS = 30
NOTE_PADS = 36

class MPK249_Plus(ControlSurface):

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
				new_knob.mapping_sensitivity = 2.0	# make knob movement speed match closer what is seen on Ableton's macro knob - easier to go from 0 to max value with 1 twist of wrist too
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
				pad_button = PadButtonElement(is_momentary = True, msg_type = MIDI_NOTE_TYPE, channel = 9, identifier = NOTE_PADS + current_pad_num, pad_num = current_pad_num, skin=self._skin, name = u'Pad_A_{}_{}'.format(j, i) )
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
				pad_button = PadButtonElement(True, msg_type = MIDI_NOTE_TYPE, channel = 9, identifier = NOTE_PADS + 48 + current_pad_num, pad_num = 48 + current_pad_num, skin=self._skin, name = u'Pad_D_{}_{}'.format(j, i) )
				current_pad_num = current_pad_num + 1
				pad_row.append( pad_button )
			pad_rows_bank_d.insert(0, pad_row) # put new row before the previous one, because the MPK2 numbers the pads starting from bottom and not top
		self._btn_pads_bank_d_matrix = ButtonMatrixElement(rows = pad_rows_bank_d, name = u'Drum_Pad_Button_Matrix')
	
	# Assign knobs to device component
	def _create_device(self):
		self._device = DeviceComponent(device_selection_follows_track_selection = True, name=u'Device', is_enabled = False)
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