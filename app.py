import time
from flask import Flask, request, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import client_secrets

app = Flask(__name__)

app.config.from_pyfile('config.py')
TOKEN_INFO = "token_info"

# setup endpoints
@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('create', _external=True))


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
    sp.user_playlist_create(user=sp.me()['id'],
                            name="testPlaylist",        # change so user can enter the details they want
                            public=True,
                            collaborative=False,
                            description="test playlist created with Spotipy")
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
    if (is_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])

    token_valid = True
    return token_info, token_valid


def create_spotify_oauth():
    """ creates a SpotifyOAuth object that can be used to authenticate requests """
    return SpotifyOAuth(
        client_id=client_secrets.return_client_id(),
        client_secret=client_secrets.return_client_secret(),
        redirect_uri=url_for('redirectPage', _external=True),
        scope="playlist-modify-public"
    )

