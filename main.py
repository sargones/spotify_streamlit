# from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import numpy as np
import pandas as pd
from streamlit import secrets

# load_dotenv()
# client_id = os.getenv("CLIENT_ID")
# client_secret = os.getenv("CLIENT_SECRET")
# print(client_id, client_secret)

# client_id = os.environ['CLIENT_ID']
# client_secret = os.environ['CLIENT_SECRET']

client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')


#functions
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials"}
    result = post(url, headers = headers, data = data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers = headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artist with this name exists...")
        return None
    return json_result[0]

def get_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = get_auth_header(token)
    result = get(url, headers = headers)
    json_result = json.loads(result.content)
    return json_result

def get_songs_by_artist(token, artist_id, market):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=market"
    headers = get_auth_header(token)
    result = get(url, headers = headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def get_albums_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
    headers = get_auth_header(token)
    result = get(url, headers = headers)
    json_result = json.loads(result.content)["items"]
    return json_result

# get token
token = get_token()
#print(token)


#Bands and IDs
Slipknot = "05fG473iIaoy82BF1aGhL8"
Electric_callboy = "1WNoKxsp715jez1Td4vthc"
Wanda = "6Kg9EvjSnEm5swmrvWCJyB"
Lorna_Shore = "6vXYoy8ouRVib302zxaxFF"

IDs = ['05fG473iIaoy82BF1aGhL8', '1WNoKxsp715jez1Td4vthc', '6Kg9EvjSnEm5swmrvWCJyB', '6vXYoy8ouRVib302zxaxFF']


id = []
name = []
genres = []
popularity = []
followers = []

for artist_id in IDs:
  artist = get_artist(token, artist_id)
  # print(artist["name"])
  # print(artist["genres"])
  # print(artist["popularity"])
  # print(artist["followers"]["total"])
  name.append(artist['name'])
  # for genre in artist["genres"]:
  #   genres.append(genre)
  genres.append(artist["genres"])
  popularity.append(artist["popularity"])
  followers.append(artist["followers"]["total"])
  id.append(artist_id)


artist_df = pd.DataFrame({"ID": id, "name": name, "genres": genres, "popularity": popularity, "followers": followers})
#print(artist_df.head(4))
artist_df.to_csv('artist_details.csv')

#search for Top10 songs
id = []
song_name = []
song_album = []
song_release_date = []
song_popularity = []
song_artist = []

for artist_id in IDs:
  for market in ['AT', 'DE', 'CH']:
    songs = get_songs_by_artist(token, artist_id, market)
    for idx, song in enumerate(songs):
        id.append(artist_id)
        song_name.append(song['name'])
        song_album.append(song['album']['name'])
        song_release_date.append(song['album']['release_date'])
        song_popularity.append(song['popularity'])
        song_artist.append(song['artists'][0]['name'])

songs_df = pd.DataFrame({"id": id, "artist": song_artist,  "song_name": song_name, "song_album": song_album, "song_release_date": song_release_date, "song_popularity": song_popularity}).drop_duplicates()
songs_df['artist'] = songs_df['artist'].replace('BABYMETAL', 'Electric Callboy')

songs_df['song_release_date'] = pd.to_datetime(songs_df['song_release_date'], format='mixed')
songs_df['song_release_date'] = pd.DatetimeIndex(songs_df['song_release_date']).year
songs_df.rename(columns={'song_release_date': 'song_release_year'}, inplace=True)
songs_df.reset_index(drop=True, inplace=True)

#print(songs_df.head(4))

#search for album details
name = []
album_type = []
total_tracks = []
release_date = []
artist_ids = []
artist_names = []


for artist_id in IDs:
    albums = get_albums_by_artist(token, artist_id)
    for album in albums:
        name.append(album["name"])
        album_type.append(album["album_type"])
        total_tracks.append(album["total_tracks"])
        release_date.append(album["release_date"])
        artist_ids.append(album["artists"][0]["id"])
        artist_names.append(album["artists"][0]["name"])

albums_df = pd.DataFrame({"name": name, "album_type": album_type, "total_tracks": total_tracks, "release_date": release_date, "artist_id": artist_ids, "artist_name": artist_names,}).drop_duplicates()
albums_df['release_date'] = pd.to_datetime(albums_df['release_date'], format='mixed')
albums_df['release_date'] = pd.DatetimeIndex(albums_df['release_date']).year
albums_df = albums_df[albums_df['album_type'] == 'album']
#print(albums_df.head(3))


##
albums_df.to_csv('albums.csv', index=False)
artist_df.to_csv('artists.csv', index=False)
songs_df.to_csv('songs.csv', index=False)

