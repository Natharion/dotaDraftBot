import json_download_parse
import os
import csv
import operator
import json

class CSV_Generator():
	GameList = []
	PickListLearning = [] #Picks+result
	PickListVerification = [] #Picks+result
	Scores = [] #just results
	HeaderLearning = []
	HeaderVerification = []
	Verification = 0 # 1 in k games will be verification game
	
	def __init__(self, Verif=10):
		if int(Verif <= 1):
			Verif = 1
		self.Verification = Verif
		
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
				
	def GetProGameList(self):
		my_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'match_data')
		for (dirpath, dirnames, filenames) in os.walk(my_path):
			self.GameList.extend(filenames)
			break
		for k in range(0,len(self.GameList)):
			self.GameList[k] = self.GameList[k].replace('.json','')
			self.GameList[k] = int(self.GameList[k])

	def GetProGames(self):
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
	
	def GetPubGameList(self, gamecount=250000):
		my_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'pub_batch_data')
		BatchList = []
		for (dirpath, dirnames, filenames) in os.walk(my_path):
			BatchList.extend(filenames)
			break
		for k in range(0, len(BatchList)):
			with open('pub_batch_data\\' + BatchList[k], encoding="utf8") as data_file:
				data = json.load(data_file)
				for a in range(0,100):
					self.GameList.append(data[a])
		for k in range(0, len(self.GameList)): #error checking, because shit happens and tends to crash
			if self.GameList[k]['avg_mmr'] is None: 
				self.GameList[k]['avg_mmr'] = 1 #games with no mmr are treated as if they had mmr of 1
		self.GameList.sort(key=lambda k: k['avg_mmr'], reverse=True)
		for k in range(0, min(len(self.GameList),gamecount)):
			Temp = []
			for i in range(0,127):
				Temp.append(0.5)
			RadiantPicks = self.GameList[k]['radiant_team'].split(',')
			DirePicks = self.GameList[k]['dire_team'].split(',')
			for i in range(0,len(RadiantPicks)):
				Temp[int(RadiantPicks[i])] = 0
			for i in range(0,len(DirePicks)):
				Temp[int(DirePicks[i])] = 0
			if self.GameList[k]['radiant_win'] is True:
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
	CSV_Generator = CSV_Generator(30)
	CSV_Generator.GetPubGameList(gamecount=50000)
	CSV_Generator.GenerateHeader()
	CSV_Generator.SaveToDisk('learning.csv', 'verification.csv')