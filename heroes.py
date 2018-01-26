import csv
import collections
import os

class DOTA_Heroes:
	Hero = collections.OrderedDict()
	def __init__(self):
		if os.path.isfile('heroes.csv'):
			with open('heroes.csv', newline='') as csvfile:
				HeroesReader = csv.DictReader(csvfile, delimiter=';')
				for row in HeroesReader:
					if row['HeroID'] != 'Unused':
						self.Hero[int(row['HeroID'])] = row['Name']
						self.Hero[row['Name']] = int(row['HeroID'])

	def InterpretValue(self, Value):
		if Value == 0.5:
			Interpretation = 'Not picked'
			return Interpretation
		Interpretation = ''
		if Value == 1:
			Interpretation = 'picked by Dire'
		if Value == 0:
			Interpretation = 'picked by Radiant'
		return Interpretation
		
	def GeneratePickList(self, RadiantPicks, DirePicks):
		result = []
		result.append(0.5)
		for k in range(1, 127): #1,2,3,4,...,124,126
			if (any(Text == self.Hero[k] for Text in RadiantPicks) or any(self.Hero[k] == self.Hero[Text] for Text in RadiantPicks)):
				result.append(0)
			elif (any(Text == self.Hero[k] for Text in DirePicks) or any(self.Hero[k] == self.Hero[Text] for Text in DirePicks)):
				result.append(1)
			else:
				result.append(0.5)
		return result
	
	def PrintPickList(self, PickList, Short=True):
		for k in range(1, len(PickList)):
			if (self.Hero[k] != 'Unused'):
				if (Short is False or PickList[k] != 0.5) is True:
					print(str(k) + ' / ' + self.Hero[k] + ': ' + self.InterpretValue(PickList[k]))
	

if __name__ == "__main__":
	DOTA_Heroes = DOTA_Heroes()