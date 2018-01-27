import json
import urllib.request
import shutil
import os
import time
import heroes
import sys
import pprint

def GetFileName(match_id):
	work_dir = os.path.dirname(os.path.abspath(__file__))
	save_folder = os.path.join(work_dir, 'match_data\\')
	match_file_name = os.path.join(save_folder, str(match_id) + '.json')
	return match_file_name

def GetBatchName(batch_number):
	work_dir = os.path.dirname(os.path.abspath(__file__))
	save_folder = os.path.join(work_dir, 'batch_data\\')
	batch_name = os.path.join(save_folder, 'match_batch_' + str(batch_number) + '.json')
	return batch_name
	
def DownloadMatchData(match_id, verify=True): #returns false if match was already on the hard drive
	match_file_name = GetFileName(match_id)
	if not hasattr(DownloadMatchData, "LastDownload"):
		DownloadMatchData.LastDownload = time.clock()
	if verify is True:
		if os.path.isfile(match_file_name) is True:
			return False
	time.sleep(max((DownloadMatchData.LastDownload+0.5)-time.clock(),0))
	print('Downloading: ' + str(match_id))
	url = 'https://api.opendota.com/api/matches/'
	full_url = url + match_id
	with urllib.request.urlopen(full_url) as url_stream, \
		open(match_file_name, 'wb') as download_file:
			shutil.copyfileobj(url_stream, download_file)
	DownloadMatchData.LastDownload = time.clock()
	return True

def ParseMatchData(match_id):
	with open(GetFileName(match_id), encoding="utf8") as data_file:
		data = json.load(data_file)
	return data

def DownloadAndParse(match_id, verify=True): #returns [match json file; true if downloaded, false otherwise]
	result = DownloadMatchData(match_id=match_id, verify=verify)
	return (ParseMatchData(match_id),result)

	
def PatchVerification(pro_match_batch, patch, stop_on_first_already_downloaded=False): #ProMatchBatch = json_file_name
	with open(pro_match_batch, encoding="utf-8") as data_file:
		pro_match_data = json.load(data_file)
		
	match_data = []
	oldest_match_id = 0
	continue_downloading = True
	for i in range(0,100):
		X = DownloadAndParse(str(pro_match_data[i]['match_id']))
		match_data.append(X[0])
		if (X[1] is False) and (stop_on_first_already_downloaded is True) is True:
			last_good_match_id = i # ID w PĘTLI
			oldest_match_id = match_data[last_good_match_id]['match_id'] #ID GRY TEST
			continue_downloading = False
			print('Match on the disk, stopping')
			break
			
		
		
		if match_data[i]['patch'] != patch:
			last_good_match_id = i # ID w PĘTLI
			oldest_match_id = match_data[last_good_match_id]['match_id'] #ID GRY
			continue_downloading = False
			break
	
	if continue_downloading is True:
		oldest_match_id = match_data[99]['match_id']
		
	return (oldest_match_id, continue_downloading)
	
def GetBatch(oldest_match_id=0, batch_number=0): #returns json file with 100 games
	print('Getting batch! ' + str(batch_number))
	match_id_list = []
	if oldest_match_id == 0:
		start_url = 'https://api.opendota.com/api/proMatches'
	else:
		start_url = 'https://api.opendota.com/api/proMatches?less_than_match_id=' + str(oldest_match_id)
	batch_name = GetBatchName(batch_number)
	with urllib.request.urlopen(start_url) as url_stream, \
			open(batch_name, 'wb') as download_file:
				shutil.copyfileobj(url_stream, download_file)
	
def GetProMatches(patch):
	batch_number = 0
	oldest_match_id = 0
	continue_downloading = True
	
	while continue_downloading is True:
		GetBatch(oldest_match_id,batch_number)
		Result = PatchVerification(GetBatchName(batch_number),patch,True)
		oldest_match_id = Result[0]
		continue_downloading = Result[1]
		batch_number = batch_number + 1
	
if __name__ == '__main__':
	GetProMatches(26)
		









