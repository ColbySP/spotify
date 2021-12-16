import pandas as pd


def getTotalMinutes(df):
    """
    :param df: Dataframe object containing spotify listening data
    :return: Integer of number of minutes listened
    """
    total_time = df['msPlayed'].sum()
    return total_time // (1000 * 60)


def getTopArtists(df, n=None):
    """
    :param df: Dataframe object containing spotify listening data
    :param n: Optional number of results returned
    :return: Dictionary object of artists and corresponding minutes listened
    """
    artists = {}
    for index, row in df.iterrows():
        if row['artistName'] in artists:
            artists[row['artistName']] += row['msPlayed'] / 60000
        else:
            artists[row['artistName']] = row['msPlayed'] / 60000

    top_artists = dict(sorted(artists.items(), key=lambda item: item[1], reverse=True))

    if n:
        first_n = {k: top_artists[k] for k in list(top_artists)[:n]}
        return first_n
    else:
        return top_artists


def getTopSongs(df, n=None):
    """
    :param df: Dataframe object containing spotify listening data
    :param n: Optional number of results returned
    :return: Dictionary object of songs and corresponding minutes listened
    """
    songs = {}
    for index, row in df.iterrows():
        if row['trackName'] in songs:
            songs[row['trackName']] += row['msPlayed'] / 60000
        else:
            songs[row['trackName']] = row['msPlayed'] / 60000

    top_songs = dict(sorted(songs.items(), key=lambda item: item[1], reverse=True))

    if n:
        first_n = {k: top_songs[k] for k in list(top_songs)[:n]}
        return first_n
    else:
        return top_songs


def getTopDays(df, n=None):
    """
    :param df: Dataframe object containing spotify listening data
    :param n: Optional number of results returned
    :return: Dictionary object of dates and corresponding minutes listened
    """
    df.index = pd.to_datetime(df.index, format='%Y-%m-%d %M:%S').strftime('%Y-%m-%d')

    dates = {}
    for index, row in df.iterrows():
        if index in dates:
            dates[index] += row['msPlayed'] / 60000
        else:
            dates[index] = row['msPlayed'] / 60000

    top_days = dict(sorted(dates.items(), key=lambda item: item[1], reverse=True))

    if n:
        first_n = {k: top_days[k] for k in list(top_days)[:n]}
        return first_n
    else:
        return top_days
