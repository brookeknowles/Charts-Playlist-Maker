# Charts-Playlist-Maker

This web app scrapes data from various music charts around the world (NZ, Australia, USA), which is then used to create Spotify playlists of the top charting songs. 

## To Run App:
### Install dependencies:
    
Run on terminal:

> pip3 install -r requirements.txt

### Get Spotify Client Secrets
- Create a [Spotify developer account](https://developer.spotify.com/)
- Create new application on https://developer.spotify.com/dashboard/applications
- Make note of your Client ID and Client Secret
- [The Spotify developer website has a good tutorial on this](https://developer.spotify.com/documentation/general/guides/authorization/app-settings/)

### Run App:

Using your Client ID and Client Secret from the previous step, set your variables in the terminal:
> export SPOTIFY_CLIENT_ID='{Your client ID}'

> export SPOTIFY_CLIENT_SECRET='{Your client secret}'

(note: 'export' should only be used for Mac or Linux machines. In Windows, replace 'export' with 'set')

Then, run the app:
> set FLASK_APP=app
> 
> flask run

## How It Works:
The first time the application is run, you will be taken to login with your Spotify account:

![Screenshot](/screenshots/LoginScreen.png)

Once logged in, you will see the homepage:

![Screenshot](/screenshots/HomePage.png)

Here, you can select which chart you want to create a playlist from:

![Screenshot](/screenshots/SelectChart.png)

Then enter a name and description for your playlist and submit:

![Screenshot](/screenshots/SubmitDetails.png)

Finally, a playlist will be created on your Spotify account, and the link to it will be embedded onto the web page for easy access

![Screenshot](/screenshots/CreatedPlaylistScreen.png)