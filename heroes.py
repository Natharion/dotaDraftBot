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


	def GeneratePickList(self, RadiantPicks, DirePicks):
		result = []
		result.append(0.5)
		for k in range(1, 127): #1,2,3,4,...,124,126
			if (any(Text == self.Hero[k] for Text in RadiantPicks) or any(self.Hero[k] == self.Hero[Text] for Text in RadiantPicks)):
				result.append(0)
				#print('Detected Radiant pick: ' + Hero[k] + ' ID: ' + str(k))
			elif (any(Text == self.Hero[k] for Text in DirePicks) or any(self.Hero[k] == self.Hero[Text] for Text in DirePicks)):
				result.append(1)
				#print('Detected Dire pick: ' + Hero[k] + ' ID: ' + str(k))
			else:
				result.append(0.5)
		return result
	
	def PrintPickList(self, PickList, Short=True):
		for k in range(1, len(PickList)):
			if (self.Hero[k] != 'Unused'):
				if (Short is False or PickList[k] != 0.5) is True:
					print(str(k) + ' / ' + self.Hero[k] + ': ' + str(PickList[k]))
	

if __name__ == "__main__":
	DOTA_Heroes = DOTA_Heroes()