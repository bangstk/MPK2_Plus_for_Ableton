#
#	DeviceComponent_MultiBank.py
#	Extension of _Framework DeviceComponent to map multiple banks at once if enough controls are available
#

from __future__ import absolute_import, print_function, unicode_literals
from _Framework.DeviceComponent import DeviceComponent

class DeviceComponent_MultiBank(DeviceComponent):

	# map more than only the selected parameter bank, if available
	# This doesn't handle things like showing names for the additional banks, but MPK2 couldn't show them anyway
	def _assign_parameters(self):
		assert self.is_enabled()
		assert self._device != None
		assert self._parameter_controls != None
		self._bank_name, banks, index = self._current_bank_details()

		# pack all parameters at current bank and above into 1 list
		# TODO: if we're bluehanding something, skip parameters that are locked by macros, to not waste any controls
		parameters = []

		for index in range (index, len(banks)):
			for parameter in banks[index]:
				parameters.append(parameter)
		
		# assign all available controls to this list until we're out of controls
		for control, parameter in zip(self._parameter_controls, parameters):
			if control != None:
				if parameter != None:
					control.connect_to(parameter)
				else:
					control.release_parameter()

		self._release_parameters(self._parameter_controls[len(parameters):])

	# return all banks instead of just the current bank, unless we're doing a best_of
	def _current_bank_details(self):
		bank_name = self._bank_name
		best_of = self._best_of_parameter_bank()
		banks = self._parameter_banks()
		if banks:
			if self._bank_index != None or not best_of:
				index = self._bank_index if self._bank_index != None else 0
				bank_name = self._parameter_bank_names()[index]
				return (bank_name, banks, index)                
			else:
				bank_name = u'Best of Parameters'
				return (bank_name, [best_of], 0)