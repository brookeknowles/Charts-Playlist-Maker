from bs4 import BeautifulSoup
import requests
import json

url = "https://www.billboard.com/charts/hot-100/"
result = requests.get(url)
soup = BeautifulSoup(result.text, "html.parser")

# print(soup.prettify())
song_list = []
artist_list = []

# GET #1 ARTIST (CURRENTLY NOT WORKING)
topArtist = soup.find_all("p", {"class": "c-tagline  a-font-primary-l a-font-primary-m@mobile-max lrv-u-color-black u-color-white@mobile-max lrv-u-margin-tb-00 lrv-u-padding-t-025 lrv-u-margin-r-150"})
# print(topArtist)

# GET #1 SONG (WORKS FINE)
topSong = soup.find("a", {"href": "#",
                          "class": "c-title__link lrv-a-unstyle-link"})
song_list.append(topSong.text)


# GET ARTISTS 2-100 (WORKS FINE)
artist = soup.findAll("span", {"class": "c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-line"
                                        "-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block a-"
                                        "truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only"
                               })
for i in range(99):
    artist_list.append(artist[i].text)


# GET SONGS 2-100 (WORKS FINE)
song = soup.findAll("h3", {"class": "c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size"
                                    "-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max "
                                    "a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only",
                           "id": "title-of-a-story"})

for i in range(99):
    song_list.append(song[i].text)