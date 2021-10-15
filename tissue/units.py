

class TissueStatus:

	fridge = 'fridge'
	transfer = 'transfer'
	orbone = 'orbone'

	def get_list(self):
		return ((self.fridge, self.fridge), (self.transfer, self.transfer), (self.orbone, self.orbone))
