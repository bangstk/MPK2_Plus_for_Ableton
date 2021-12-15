#
#	MPK261_Plus.py
#	Main controller code for MPK261
#

from __future__ import absolute_import, print_function, unicode_literals
import Live
from MPK2_Plus_MPK249.MPK249_Plus import MPK249_Plus

# hardware and layout definitions
SYX_DEVICE_ID = 0x25

# MPK261 is identical to MPK249 except for the sysex id, so inherit while changing the id.
class MPK261_Plus(MPK249_Plus):

	sysex_device_id = SYX_DEVICE_ID

	def __init__(self, *a, **k):
		super(MPK261_Plus, self).__init__(*a, **k)
