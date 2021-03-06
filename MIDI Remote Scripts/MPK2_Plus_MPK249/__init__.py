#
#	__init__.py
#	Init code for MPK249
#

from __future__ import absolute_import, print_function, unicode_literals
from .MPK249_Plus import MPK249_Plus
from _Framework.Capabilities import controller_id, inport, outport, CONTROLLER_ID_KEY, PORTS_KEY, NOTES_CC, SCRIPT, REMOTE

def get_capabilities():
	return {CONTROLLER_ID_KEY: controller_id(vendor_id=2536, product_ids=[36], model_name=u'MPK249 Plus'),
	 PORTS_KEY: [inport(props=[NOTES_CC, SCRIPT, REMOTE]), outport(props=[SCRIPT, REMOTE])]}

def create_instance(c_instance):
	return MPK249_Plus(c_instance)