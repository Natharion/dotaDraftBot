import json_download_parse
import os
import csv

class CSV_Generator():
	GameList = []
	PickList = []
	Scores = []
	
	def __init__(self):
		self.GetGameList()
		self.GetGames()
		self.ParseGames()
		
	def GetGameList(self):
		my_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'match_data')
		for (dirpath, dirnames, filenames) in os.walk(my_path):
			self.GameList.extend(filenames)
			break
		for k in range(0,len(self.GameList)):
			self.GameList[k] = self.GameList[k].replace('.json','')
			self.GameList[k] = int(self.GameList[k])

	def GetGames(self):
		for k in range(0,len(self.GameList)):
			self.GameList[k] = json_download_parse.ParseMatchData(self.GameList[k])
	
	def ParseGames(self):
		for k in range(0,len(self.GameList)):
			Temp = []
			for i in range(0,127):
				Temp.append(0.5)
			for i in range(0,5):
				Temp[self.GameList[k]['players'][i]['hero_id']] = 0
			for i in range(5,10):
				Temp[self.GameList[k]['players'][i]['hero_id']] = 1
			self.PickList.append(Temp)
			
			if self.GameList[k]['radiant_win'] is True:
				self.Scores.append(0)
			else:
				self.Scores.append(1)
if __name__ == '__main__':
	CSV_Generator = CSV_Generator()
	for k in range(0,len(CSV_Generator.PickList)):
		print('Match ID: ' + str(CSV_Generator.GameList[k]['match_id']) + ' / Dire Win:' + str(CSV_Generator.Scores[k]))