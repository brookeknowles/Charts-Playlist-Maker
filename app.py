import time

from flask import Flask, request, url_for, session, redirect, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
from main import get_NZ_top_40, get_billboard_hot_100, get_aria_top_50

app = Flask(__name__)

app.config.from_pyfile('config.py')
TOKEN_INFO = "token_info"

global playlist_id
global embedded_playlist_url
global playlist_url


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


@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        playlist_name = request.form['playlist_name'].strip()
        playlist_description = request.form['playlist_description'].strip()
        chart = request.form['chart'].strip()
        create(chart, playlist_name, playlist_description)
        return render_template('created.html', value=embedded_playlist_url)
    else:
        return render_template('index.html')


def create(chart, playlist_name, playlist_description):
    """ creates new spotify playlist for user currently logged in, based on their choices from the form on homepage """
    try:
        session['token_info'], authorized = get_token()
        session.modified = True
    except:
        print("user not logged in")
        return redirect('/')

    sp = spotipy.Spotify(auth=session.get('token_info').get('access_token'))
    playlist = sp.user_playlist_create(user=sp.me()['id'],
                                       name=playlist_name,
                                       public=True,
                                       collaborative=False,
                                       description=playlist_description)

    global playlist_url
    playlist_url = playlist['external_urls']['spotify']
    global embedded_playlist_url
    embedded_playlist_url = make_embedded_url(playlist_url)

    global playlist_id
    playlist_id = playlist['id']

    add_songs_to_playlist(get_uri_from_spotify(chart))

    return "created playlist"

def make_embedded_url(url):
    """ This function turns the URL of the created playlist into the format used for embedding a playlist """
    split_string_tuple = url.partition(".com/")
    embedded = split_string_tuple[0] + split_string_tuple[1] + "embed/" + split_string_tuple[2] + "?utm_source=generator"
    return embedded

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
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
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
    elif selected_chart == "AU":
        num_chart_entries = 50
        chart_data = get_aria_top_50()
    else:  # will be BBH100, need to change later to catch error for incorrect input but this works for now
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
