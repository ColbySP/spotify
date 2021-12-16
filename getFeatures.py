from analysis import getTopSongs
import pandas as pd
import requests
import spotipy

username = 'YOUR SPOTIFY USERNAME'
client_id = 'YOUR CLIENT ID'
client_secret = 'YOUR SECRET KEY'
redirect_uri = 'http://localhost:7777/callback'
scope = 'user-read-recently-played'

token = spotipy.util.prompt_for_user_token(username=username,
                                           scope=scope,
                                           client_id=client_id,
                                           client_secret=client_secret,
                                           redirect_uri=redirect_uri)


def get_id(track_name, token):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer ' + token,
    }
    params = [
        ('q', track_name),
        ('type', 'track'),
    ]
    try:
        response = requests.get('https://api.spotify.com/v1/search',
                                headers=headers, params=params, timeout=5)
        json = response.json()
        first_result = json['tracks']['items'][0]
        track_id = first_result['id']
        return track_id
    except:
        return None


def get_features(track_id, token):
    sp = spotipy.Spotify(auth=token)
    try:
        features = sp.audio_features([track_id])
        return features[0]
    except:
        return {}


df = pd.read_csv('compiled_data.csv').set_index('endTime')
top_songs = getTopSongs(df, 500).keys()

worked = []
feature_df = pd.DataFrame()
for song in top_songs:
    print('getting features for {}...'.format(str(song)))
    # get song features
    id = get_id(song, token)
    features = get_features(id, token)

    # only add songs that have relevant features
    if len(features) > 0:
        # format data into pandas series to be combined into Dataframe
        data = pd.DataFrame.from_dict(features, orient='index').T
        feature_df = feature_df.append(data)
        worked.append(song)
    else:
        pass

# convert the index
feature_df.index = worked
feature_df.to_csv('feature_data.csv')
