import time

from flask import Flask, request, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import client_secrets
from main import get_NZ_top_40, get_billboard_hot_100

app = Flask(__name__)

app.config.from_pyfile('config.py')
TOKEN_INFO = "token_info"

global playlist_id


@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route('/redirect')
def redirect_page():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('home', _external=True))


@app.route('/home')
def home():
    return 'Homepage!'


@app.route('/create')
def create():
    """ creates new spotify playlist for user currently logged in """
    try:
        session['token_info'], authorized = get_token()
        session.modified = True
    except:
        print("user not logged in")
        return redirect('/')

    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    playlist = sp.user_playlist_create(user=sp.me()['id'],
                            name="testPlaylist",        # change so user can enter the details they want
                            public=True,
                            collaborative=False,
                            description="test playlist created with Spotipy")

    global playlist_id
    playlist_id = playlist['id']

    add_songs_to_playlist(get_uri_from_spotify("US"))  # TODO: change to variable that allows user to choose which chart

    return "created playlist"


def get_token():
    """ checks to see if token is valid and gets a new token if not """
    token_valid = False
    token_info = session.get(TOKEN_INFO, {})

    # checking if token has expired
    if not (session.get('token_info', False)):
        token_valid = False
        return token_info, token_valid

    # checking if token has expired
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60

    # refresh token if it has expired
    if is_expired:
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])

    token_valid = True
    return token_info, token_valid


def create_spotify_oauth():
    """ creates a SpotifyOAuth object that can be used to authenticate requests """
    return SpotifyOAuth(
        client_id=client_secrets.return_client_id(),
        client_secret=client_secrets.return_client_secret(),
        redirect_uri=url_for('redirect_page', _external=True),
        scope="playlist-modify-public"
    )


def get_uri_from_spotify(selected_chart):
    """ gets a list of URIs from spotify based off the chart data returned from the get_NZ_top_40()
     or get_billboard_hot_100() functions. """

    try:
        session['token_info'], authorized = get_token()
        session.modified = True
    except:
        print("user not logged in")
        return redirect('/')

    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))

    if selected_chart == "NZ":
        num_chart_entries = 40
        chart_data = get_NZ_top_40()
    else:    # will be BBH100, need to change later to catch error for incorrect input but this works for now
        num_chart_entries = 100
        chart_data = get_billboard_hot_100()

    artists_list = []
    for i in range(num_chart_entries):
        artists_list.append(chart_data[i]['Artist'])

    songs_list = []
    for i in range(num_chart_entries):
        songs_list.append(chart_data[i]['Track'])

    uris_list = []
    for i in range(num_chart_entries):
        search_info = sp.search(q='artist:' + artists_list[i] + ' track:' + songs_list[i], type='track')
        track_uri = search_info["tracks"]["items"][0]["uri"]
        uris_list.append(track_uri)

    return uris_list


def add_songs_to_playlist(uris_list):
    """ adds the songs from the charts to the playlist that was created """
    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    sp.playlist_add_items(playlist_id=playlist_id, items=uris_list, position=None)

