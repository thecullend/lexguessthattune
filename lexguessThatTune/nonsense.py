import spotipy
import spotipy.util as util
import requests
import json

scope = 'user-library-read'

CLIENT_ID='c295be00d2ef4690973209fed490463e'
CLIENT_SECRET='9b0202848ee143afad3f9846a2f2655d'
redirect_uri='http://locallhost/'

username="1fgsvzfz62lz1ri517bwo3c2b"
lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'
artist_uri = 'spotify:artist:7GaxyUddsPok8BuhxN6OUW'

token = util.oauth2.SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

cache_token = token.get_access_token()

spotify = spotipy.Spotify(cache_token)
results = spotify.artist_top_tracks(artist_uri)

url = 'https://nx4evy0tf4.execute-api.us-east-1.amazonaws.com/prod/getsongs'

response = requests.get(url)
string_data = response.content.decode("utf-8")
json_data = string_data.replace("'", "\"")
json_dict = json.loads(json_data)

json

print (json_dict)


for track in results['tracks'][:10]:
    print ('track    : ' + track['name'])
    if (track['preview_url'] != None):
    	print ('audio    : ' + track['preview_url'])
    print ('cover art: ' + track['album']['images'][0]['url'])
    print()
