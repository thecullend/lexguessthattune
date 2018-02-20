# -*- coding: utf-8 -*-

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import boto3
import json
import spotipy
import os
import urllib2
import pydub
from pydub import AudioSegment
from pprint import pprint


scope = 'user-library-read'
CLIENT_ID='b5bc60fcca844bf4a4f53dfdbe5a1740'
CLIENT_SECRET='780122ebe21646f686d51a160c1b7d02'
username='hd2mu909nudbei8e23skwbjel'


client_credentials_manager = SpotifyClientCredentials(client_id = CLIENT_ID, client_secret = CLIENT_SECRET)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

uri = 'spotify:user:spotifycharts:playlist:37i9dQZEVXbMDoHDwVN2tF'
username = uri.split(':')[2]
playlist_id = uri.split(':')[4]

results = sp.user_playlist(username, playlist_id)
json_data = json.dumps(results, indent=4)
data = json.loads(json_data)

aud_dir = 'http://s3.amazonaws.com/mediasourcebucket/'

s3 = boto3.client('s3')


def handler (event, context):
	for i in range(0,50):
		if data["tracks"]["items"][i]["track"]["preview_url"] != None:
			name = data["tracks"]["items"][i]["track"]["name"] + ".mp3"

			os.chdir('/tmp')     	
			with open(name, 'w') as openmp3:
				file = urllib2.urlopen(data["tracks"]["items"][i]["track"]["preview_url"])
				file2 = file.read()
				'''
				FFMPEG Conversions
				alexa_mp3 = AudioSegment.from_file(file, format="mp3", parameters =["-ar", "16000", "-ab", "48k", "-codec:a", "libmp3lame", "-ac", "1"])
				print alexa_mp3

				file2 = alexa_mp3.export().read()
				#print file2
				'''

				openmp3.write(file2)


				s3.upload_file (name,"mediasourcebucket", Key =name, 
					ExtraArgs = {
					'ACL' : 'public-read',
					"Metadata": {"Title": "name"}
						}
					)
				
				openmp3.close()
			


			
	return {
		"statusCode": 200
		}

