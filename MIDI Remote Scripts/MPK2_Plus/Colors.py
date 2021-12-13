#
#	Colors.py
#	Define color classes & Ableton-to-MPK2 pad color mappings
#

from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ButtonElement import Color

# Color class which will set drum pad color and make it blink
class BlinkColor(Color):
	def __init__(self, midi_value = 0, *a, **k):
		super(BlinkColor, self).__init__(midi_value, *a, **k)
		
	def draw(self, interface):
		interface.send_value(self.midi_value, channel = 9)

	# TODO: Pad Blinker
	# It looks like all other fancy keyboards have blinking built in to their hardware. MPK2 doesn't.
	# Search _Framework for some kind of repeating timer to toggle note on/off to make pad blink.
	# Preferably based on tempo...
	# Until then BlinkColor will behave exactly the same as Color

	# def draw(self, interface):
		# blinker code goes here

# Define human readable color names for MPK2's pad color choices
# The color index is used to create the correct sysex message in the above color classes
class MPK2PadColors:
	BLACK = Color(0)
	RED = Color(1)
	ORANGE = Color(2)
	YELLOW = Color(3)	# Called 'Amber' by MPK2's settings
	YELLOW_GREEN = Color(4)	# Called 'Yellow' by MPK2's settings
	GREEN = Color(5)
	GREEN_BLUE = Color(6)
	AQUA = Color(7)	# Sky blue, called 'Aqua' by MPK2's settings
	LT_BLUE = Color(8)	# Darker blue than AQUA but lighter than BLUE
	BLUE = Color(9)
	PURPLE = Color(10)
	PINK = Color(11)
	HOT_PINK = Color(12)
	LT_PURPLE = Color(13)
	LT_GREEN = Color(14)	# Very pale blue/green
	LT_PINK = Color(15)
	GREY = Color(16)	# Not quite as bright as white, but as close as we can get

class MPK2PadBlinkColors:
	RED = Color(1)
	ORANGE = Color(2)
	YELLOW = Color(3)
	YELLOW_GREEN = Color(4)
	GREEN = Color(5)
	HOT_PINK = Color(12)

# Color table used to map Ableton RGB color to an MPK2 pad color index
LIVE_RGB_VALUE_TO_MIDI_VALUE_TABLE = {
	# Stock Ableton 10+ clip color set
	0xffb1be: 15, 0xffb249:  2, 0xd6ac4e:  2, 0xfaf7a5:  3, 0xc5fb1a:  4, 0x38ff4a:  5, 0x45ffb5:  6, 0x7effed: 14, 0xa9d4ff: 13, 0x87a6ec: 13, 0xafbfff: 13, 0xe6a2ee: 15, 0xed85bc: 15, 0xffffff: 16,
	0xff5757:  1, 0xf77b1e:  2, 0xb49473:  2, 0xfff255:  3, 0xa2ff89: 14, 0x47c80c:  5, 0x0bc4b5:  7, 0x37ecff:  7, 0x32b1f0:  7, 0x0c84c5:  8, 0xb3a2ee: 13, 0xb3a2ee: 15, 0xff5adb: 12, 0xf9f9f9: 16,
	0xeb978e: 15, 0xffb995: 15, 0xe5cfac:  2, 0xf2ffc6:  3, 0xe9f2cd:  3, 0xd8e4b0:  4, 0xd1e4cb:  4, 0xe5feed: 16, 0xe6f8fc: 16, 0xe7eaf5: 16, 0xeee8f6: 16, 0xd7ccf2: 13, 0xfbfafb: 16, 0xe3e3e3: 16,
	0xe4ccc9: 16, 0xceab8d:  2, 0xbfb1a1:  2, 0xd8d5a5:  3, 0xacc40b:  4, 0xa2c780:  4, 0xc6e2de: 14, 0xd8e1e8: 16, 0xc3d3e1: 13, 0xc0c8e5: 13, 0xdad3e0: 16, 0xe7dce7: 16, 0xd9aec3: 15, 0xaeaeae: 16,
	0xc05656:  1, 0xbb6d50:  1, 0x926654:  2, 0xdec712:  2, 0x98aa2c:  4, 0x6cb44c:  4, 0x0faa9b:  7, 0x2a769e:  8, 0x243ba9:  9, 0x4a6bb6: 13, 0x8d7cc4: 10, 0xbd7cc4: 11, 0xd7598c: 12, 0x4b4b4b: 16,

	# Stock Ableton 9- clip color set
	0xed4325:  1, 0xbd6100:  2, 0xb08b00:  3, 0x85961f:  4, 0x539f31:  5, 0x0a9c8e:  7, 0x007abd:  8, 0x0303ff:  9, 0x2f52a2:  9, 0x624bad: 10, 0x7b7b7b: 16, 0x3c3c3c: 16,
	0xff0505:  1, 0xbfba69:  2, 0xa6be00:  4, 0x7ac634:  4, 0x3dc300:  5, 0x00bfaf:  7, 0x10a4ee:  7, 0x5480e4: 13, 0x886ce4: 10, 0xa34bad: 11, 0xb73d69:  1, 0x965735:  2,
	0xf66c03:  2, 0xbffb00:  4, 0x87ff67: 14, 0x1aff2f:  5, 0x25ffa8: 14, 0x5cffe8: 14, 0x19e9ff:  7, 0x8bc5ff: 13, 0x92a7ff: 13, 0xb88dff: 13, 0xd86ce4: 11, 0xff39d4: 12,
	0xffa529:  2, 0xfff034:  3, 0xe3f403:  4, 0xdbc300:  2, 0xbe9d63:  2, 0x89b47d:  4, 0x88c2ba:  7, 0x9bb3c4: 16, 0x85a5c2: 13, 0xc68b7c: 15, 0xf14080: 12, 0xff94a6: 15,
	0xffa374: 15, 0xffee9f:  3, 0xd2e498:  4, 0xbad074:  4, 0xa9a9a9: 16, 0xd4fde1: 14, 0xcdf1f8: 14, 0xb9c1e3: 13, 0xcdbbe4: 15, 0xd0d0d0: 16, 0xdfe6e5: 16, 0xffffff: 16
}

# Color table used to match an Ableton RGB color to its closest MPK2 pad color index
# Only used if a color is not found in the above table
MIDI_VALUE_TO_RGB_COLOR_TABLE = (
	(0, 0x000000),	# Off
	(1, 0xFF0000),	# Red
	(2, 0xFFC000),	# Orange
	(3, 0xFFFF00),	# Amber (Actually yellow)
	(4, 0xC6FF00),	# Yellow (Actually greenish yellow)
	(5, 0x00FF00),	# Green
	(6, 0x00FF96),	# Green Blue
	(7, 0x00C8FF),	# Aqua
	(8, 0x0080FF),	# Lt Blue
	(9, 0x0000FF),	# Blue
	(10, 0x8040FF),	# Purple
	(11, 0xC800FF),	# Pink
	(12, 0xFF00AE),	# Hot Pink
	(13, 0x8080FF),	# Lt Purple
	(14, 0x80FFB4),	# Lt Green
	(15, 0xFFA8FF),	# Lt Pink
	(16, 0xD2D2D2),	# Grey
)
