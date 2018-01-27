import json_download_parse
import os
import csv

class CSV_Generator():
	GameList = []
	PickList = [] #Picks+result
	Scores = [] #just results
	Header = []
	VerificationRatio = 0.0
	
	def __init__(self, ratio=0.2):
		self.GetGameList()
		self.GetGames()
		self.GenerateHeader()
		VerificationRatio = ratio
		
	def GenerateHeader(self):
		self.Header.append(len(self.PickList))
		self.Header.append(len(self.PickList[1]))
			
	def SaveToDisk(self, TrainingDataFile):
		with open(TrainingDataFile, 'w', newline='', encoding="utf-8") as CSV_File:
			CSV_Writer = csv.writer(CSV_File, dialect='excel')
			CSV_Writer.writerow(self.Header)
			for k in range(0,len(self.PickList)):
				CSV_Writer.writerow(self.PickList[k])
				
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
			GameBeingParsed = json_download_parse.ParseMatchData(self.GameList[k])
			Temp = []
			for i in range(0,127):
				Temp.append(0.5)
			for i in range(0,5):
				Temp[GameBeingParsed['players'][i]['hero_id']] = 0
			for i in range(5,10):
				Temp[GameBeingParsed['players'][i]['hero_id']] = 1
			
			
			if GameBeingParsed['radiant_win'] is True:
				self.Scores.append(0)
				Temp.append(0)
			else:
				self.Scores.append(1)
				Temp.append(1)
			self.PickList.append(Temp)
			
			
if __name__ == '__main__':
	CSV_Generator = CSV_Generator()
	CSV_Generator.SaveToDisk('scores.csv')