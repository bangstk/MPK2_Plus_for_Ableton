#	MPK2 Better Ableton Mapping by Trov
#
#	Elements maps the physical MIDI CCs and Notes to Python objects usable by the main control surface code
#
from __future__ import absolute_import, print_function, unicode_literals
import Live
from ableton.v2.base import depends
from ableton.v2.control_surface import MIDI_CC_TYPE, MIDI_NOTE_TYPE, PrioritizedResource
from ableton.v2.control_surface.elements import ButtonElement, ButtonMatrixElement, EncoderElement

NAV_CC_START = 60
TRANSPORT_CC_START = 114

NUM_FADERS = 8
KNOBS_CC_START = 50
FADERS_CC_START = 40
BUTTONS_CC_START = 30
NUM_FADER_BANKS = 3

SESSION_WIDTH = 4
SESSION_HEIGHT = 4
SESSION_WIDTH_WIDE = 8
SESSION_HEIGHT_WIDE = 2
DRUMS_WIDTH = 4
DRUMS_HEIGHT = 8
PADS_NOTE_START = 36
PADS_NOTE_START_A = 36
PADS_NOTE_START_B = 52
PADS_NOTE_START_C = 68
PADS_NOTE_START_D = 84
NUM_PAD_BANKS = 4

@depends(skin=None)
def create_button(identifier, name, msg_type = MIDI_CC_TYPE, channel = 0, **k):
	return ButtonElement(True, msg_type, channel, identifier, name = name, **k)

def create_encoder(identifier, name, channel = 0, **k):
	return EncoderElement(MIDI_CC_TYPE, channel, identifier, Live.MidiMap.MapMode.relative_smooth_two_compliment, name = name, **k)

class Elements(object):
	def __init__(self, *a, **k):
		super(Elements, self).__init__(*a, **k)
		
		# transport buttons
		self.loop_button = create_button(TRANSPORT_CC_START, u'Loop_Button')
		self.rw_button = create_button(TRANSPORT_CC_START + 1, u'Rewind_Button')
		self.ff_button = create_button(TRANSPORT_CC_START + 2, u'Forward_Button')
		self.stop_button = create_button(TRANSPORT_CC_START + 3, u'Stop_Button')
		self.play_button = create_button(TRANSPORT_CC_START + 4, u'Play_Button')
		self.record_button = create_button(TRANSPORT_CC_START + 5, u'Record_Button')
		# self.preview_button = create_button(???, u'Preview_Button')
		
		# nav buttons
		self.up_button = create_button(NAV_CC_START, u'Up_Button', channel = 1)
		self.down_button = create_button(NAV_CC_START + 1, u'Down_Button', channel = 1)
		self.left_button = create_button(NAV_CC_START + 2, u'Left_Button', channel = 1)
		self.right_button = create_button(NAV_CC_START + 3, u'Right_Button', channel = 1)
		self.shift_button = create_button(NAV_CC_START + 4, u'Shift_Button', channel = 1, resource_type = PrioritizedResource)
		
		# knobs - 3 banks of 8
		pots_row = []
		for bank in xrange(0, NUM_FADER_BANKS):
			for index in xrange(0, NUM_FADERS):
				pots_row.append(create_encoder(KNOBS_CC_START + index, u'Pot_{}'.format(index), channel = bank))
		
		self.pots = ButtonMatrixElement(rows = [pots_row], name=u'Pots')
		
		# faders - 3 banks of 8 - using Bank C Fader 8 as Master
		faders_row = []
		for bank in xrange(0, NUM_FADER_BANKS):
			for index in xrange(0, NUM_FADERS):
				if index < (NUM_FADERS - 1) and bank < NUM_FADER_BANKS:
					faders_row.append(create_encoder(FADERS_CC_START + index, u'Fader_{}'.format(index), channel = bank))
		
		self.faders = ButtonMatrixElement(rows = [faders_row], name=u'Faders')
		self.master_fader = create_encoder(FADERS_CC_START + NUM_FADERS - 1, u'Master_Fader', channel = 2)
		
		# buttons under faders - 3 banks of 8
		buttons_row = []
		for bank in xrange(0, NUM_FADER_BANKS):
			for index in xrange(0, NUM_FADERS):
				buttons_row.append(create_encoder(BUTTONS_CC_START + index, u'Fader_Button_{}'.format(index), channel = bank))
				
		self.fader_buttons = ButtonMatrixElement(rows = [buttons_row], name=u'Fader_Button')
		
		# pads
		
		# init a 4x4 grid of CC's - same for all 4 banks - start with pad numbers		
		PADS_NOTES_SESSION = (	(48, 49, 50, 51), 
								(44, 45, 46, 47),
								(40, 41, 42, 43),
								(36, 37, 38, 39)	)
								
		PADS_NOTES_SESSION_WIDE = (	(64, 65, 66, 67, 56, 57, 58, 59), 
									(60, 61, 62, 63, 52, 53, 54, 55)	)
								
		PADS_NOTES_DRUMS = (	(96, 97, 98, 99), 
								(92, 93, 94, 95),
								(88, 89, 90, 91),
								(84, 85, 86, 87),
								(80, 81, 82, 83), 
								(76, 77, 78, 79),
								(72, 73, 74, 75),
								(68, 69, 70, 71)	)
		
		#for i in xrange(SESSION_HEIGHT):
		#	for j in range(SESSION_WIDTH):
		#		PADS_NOTES_SESSION[i][j] = PADS_NOTES_SESSION[i][j] + PADS_NOTE_START_A
		#		
		#for i in xrange(SESSION_HEIGHT_WIDE):
		#	for j in range(SESSION_WIDTH_WIDE):
		#		PADS_NOTES_SESSION_WIDE[i][j] = PADS_NOTES_SESSION_WIDE[i][j] + PADS_NOTE_START_A
		#		
		#for i in xrange(DRUMS_HEIGHT):
		#	for j in range(DRUMS_WIDTH):
		#		PADS_NOTES_SESSION[i][j] = PADS_NOTES_DRUMS[i][j] + PADS_NOTE_START_C
		#
		# 2 separate session bank, one drum bank split across 2
		self.clip_launch_matrix = ButtonMatrixElement(rows=[ [ create_button(identifier, name=u'Pad_{}_{}'.format(col_index, row_index), msg_type = MIDI_NOTE_TYPE, channel = 9) for col_index, identifier in enumerate(row) ] for row_index, row in enumerate(PADS_NOTES_SESSION) ], name=u'Clip_Launch_Matrix')
		#self.clip_launch_matrix_wide = ButtonMatrixElement(rows=[ [ create_button(identifier, name=u'Pad_B_{}_{}'.format(col_index, row_index), channel=9) for col_index, identifier in enumerate(row) ] for row_index, row in enumerate(PADS_NOTES_SESSION_WIDE) ],  name=u'Clip_Launch_Matrix_Wide')
		self.drum_pads_matrix = ButtonMatrixElement(rows=[ [ create_button(identifier, name=u'Drum_Pad_{}_{}'.format(col_index, row_index), msg_type = MIDI_NOTE_TYPE, channel = 9) for col_index, identifier in enumerate(row) ] for row_index, row in enumerate(PADS_NOTES_SESSION_WIDE) ], name=u'Drum_Pads_Matrix')
		#self.clip_launch_matrix = ButtonMatrixElement(rows = pads_session_rows, name=u'Clip_Launch_Matrix')
		#self.drum_pads_matrix = ButtonMatrixElement(rows = pads_drum_rows, name=u'Drum_Pads')
		
		