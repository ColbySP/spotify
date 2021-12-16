# imports
from sklearn.neighbors import LocalOutlierFactor
import pandas as pd
import requests
import spotipy

SONG_TITLE = 'ENTER SONG TITLE HERE'


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


def get_features(track_name, token):
    track_id = get_id(track_name, token)
    sp = spotipy.Spotify(auth=token)
    try:
        features = sp.audio_features([track_id])
        return features[0]
    except:
        return {}


# load personal data
df = pd.read_csv('feature_data.csv').set_index('title')

# add song in question
features = get_features(SONG_TITLE, token)
data = pd.DataFrame.from_dict(features, orient='index').T
df = df.append(data)
df.rename(index={0: SONG_TITLE}, inplace=True)

# prepare data for modeling
df = df[
    ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness',
     'valence', 'tempo', 'duration_ms', 'time_signature']]

# instantiate the model
neigh = LocalOutlierFactor()

# make predictions
predictions = neigh.fit_predict(df.values[:100])

if predictions[-1] == -1:
    print('Unlikely that you enjoy the song ' + SONG_TITLE)
else:
    print('You may enjoy ' + SONG_TITLE)

# show similar songs
neigh.fit(df.values)
features = df.iloc[-1].values.reshape(1, -1)
indices = neigh.kneighbors(features, n_neighbors=6)[1]
print('\nMost Similar Matches Include:')
print(*df.index.values[indices][0][1:], sep=', ')
