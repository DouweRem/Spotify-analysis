"""
    Downloads a spotify playlists and outputs it as a playlist type object
"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import os
import time



# Authentication - without user
cid = 'XXXXXXX'
secret = 'XXXXXXX'

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)



def download_metadata(playlist_url, force_download=False):
    """
    Downloads the metadata of a spotify playlist and outputs it as a pandas dataframe
    :param playlist_url: direct link to the playlist
    :param force_download: if True, will download the playlist metadata again even if it already exists
    :return: dataframe containing the metadata of the playlist
    """

    # Get current directory
    current_dir = os.getcwd()

    playlist_URI = playlist_url.split("/")[-1].split("?")[0]
    playlist = sp.playlist(playlist_URI)
    playlist_name = playlist['name']

    # Check if playlist already exists
    file_bool = os.path.exists(current_dir + "\\" + "playlist_data" + "\\" + playlist_name + ".csv")

    if file_bool and not force_download:
        print("Loading data from file")
        df = pd.read_csv(current_dir + "\\" + "playlist_data" + "\\" + playlist_name + ".csv")
        return df

    elif file_bool:
        print("File already exists, but force_download is True")

    else:
        print("No file found, downloading data")

    results = playlist["tracks"]
    tracks = results["items"]

    # Extend the list of tracks to get all of the tracks in the playlist
    while results["next"]:
        results = sp.next(results)
        tracks.extend(results["items"])

    tick = time.time()

    track_name = []
    track_uri = []
    track_album = []
    track_album_uri = []
    track_artist = []
    track_artist_uri = []
    track_duration = []  # in ms
    track_add_date = []
    track_explicit = []
    track_popularity = []
    track_danceability = []
    track_energy = []
    track_key = []
    track_loudness = []
    track_mode = []
    track_speechiness = []
    track_acousticness = []
    track_instrumentalness = []
    track_liveness = []
    track_valence = []
    track_tempo = []
    track_time_signature = []

    for track in tracks:
        track_name.append(track["track"]["name"])
        track_uri.append(track["track"]["uri"])
        track_album.append(track["track"]["album"]["name"])
        track_album_uri.append(track["track"]["album"]["uri"])
        track_artist.append(track["track"]["artists"][0]["name"])
        track_artist_uri.append(track["track"]["artists"][0]["uri"])
        track_duration.append(track["track"]["duration_ms"])
        track_add_date.append(track["added_at"])
        track_explicit.append(track["track"]["explicit"])
        track_popularity.append(track["track"]["popularity"])

        # Get the audio features for the track
        audio_features = sp.audio_features(track_uri[-1])[0]

        track_danceability.append(audio_features["danceability"])
        track_energy.append(audio_features["energy"])
        track_key.append(audio_features["key"])
        track_loudness.append(audio_features["loudness"])
        track_mode.append(audio_features["mode"])
        track_speechiness.append(audio_features["speechiness"])
        track_acousticness.append(audio_features["acousticness"])
        track_instrumentalness.append(audio_features["instrumentalness"])
        track_liveness.append(audio_features["liveness"])
        track_valence.append(audio_features["valence"])
        track_tempo.append(audio_features["tempo"])
        track_time_signature.append(audio_features["time_signature"])

    df = pd.DataFrame({"name": track_name,
                       "uri": track_uri,
                       "album": track_album,
                       "album_uri": track_album_uri,
                       "artist": track_artist,
                       "artist_uri": track_artist_uri,
                       "duration": track_duration,
                       "add_date": track_add_date,
                       "explicit": track_explicit,
                       "popularity": track_popularity,
                       "danceability": track_danceability,
                       "energy": track_energy,
                       "key": track_key,
                       "loudness": track_loudness,
                       "mode": track_mode,
                       "speechiness": track_speechiness,
                       "acousticness": track_acousticness,
                       "instrumentalness": track_instrumentalness,
                       "liveness": track_liveness,
                       "valence": track_valence,
                       "tempo": track_tempo,
                       "time_signature": track_time_signature})

    df.to_csv(current_dir + "\\" + "playlist_data" + "\\" + playlist_name + ".csv")

    tock = time.time()
    print(f'Time taken: {tock - tick} s, total tracks: {len(tracks)}')
    return df


if __name__ == '__main__':
    df = download_metadata('https://open.spotify.com/playlist/598bwDA4m4zuo7s1DlLrR2?si=e24c81cf6968452f')
    print(df)