import json_download_parse
import os
import csv

class CSV_Generator():
	GameList = []
	PickListLearning = [] #Picks+result
	PickListVerification = [] #Picks+result
	Scores = [] #just results
	HeaderLearning = []
	HeaderVerification = []
	Verification = 0 # 1 in k games will be verification game
	
	def __init__(self, Verif=10):
		self.GetGameList()
		if int(Verif <= 1):
			Verif = 1
		self.Verification = Verif
		self.GetGames()
		self.GenerateHeader()
		
	def GenerateHeader(self):
		self.HeaderLearning.append(len(self.PickListLearning))
		self.HeaderLearning.append(len(self.PickListLearning[1]))
		self.HeaderVerification.append(len(self.PickListVerification))
		self.HeaderVerification.append(len(self.PickListVerification[1]))
		
	def SaveToDisk(self, TrainingDataFile='learning.csv', VerificationDataFile='verification.csv'):
		with open(TrainingDataFile, 'w', newline='', encoding="utf-8") as CSV_File:
			CSV_Writer = csv.writer(CSV_File, dialect='excel')
			CSV_Writer.writerow(self.HeaderLearning)
			for k in range(0,len(self.PickListLearning)):
				CSV_Writer.writerow(self.PickListLearning[k])
		with open(VerificationDataFile, 'w', newline='', encoding="utf-8") as CSV_File:
			CSV_Writer = csv.writer(CSV_File, dialect='excel')
			CSV_Writer.writerow(self.HeaderVerification)
			for k in range(0,len(self.PickListVerification)):
				CSV_Writer.writerow(self.PickListVerification[k])
				
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
			if (k % self.Verification) == 0:
				self.PickListVerification.append(Temp)
			else:
				self.PickListLearning.append(Temp)
			
			
if __name__ == '__main__':
	CSV_Generator = CSV_Generator()
	CSV_Generator.SaveToDisk('learning.csv', 'verification.csv')