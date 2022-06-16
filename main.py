from bs4 import BeautifulSoup
import requests


def get_billboard_hot_100():
    """ Gets the data from the Billboard Hot 100 website, and then creates a JSON object with all the relevant
    information """

    url = "https://www.billboard.com/charts/hot-100/"
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    soup.find("div", class_="lxml")

    # stripping punctuation so spotify doesn't pack a sad. may need to add an if clause later so that I can keep
    # punctuation for display on web page
    song_list = [strip_punctuation(result.text.strip()) for result in soup.select(
        "div.chart-results-list > div.o-chart-results-list-row-container > ul.o-chart-results-list-row > "
        "li:nth-child(4) > ul > li:nth-child(1) h3")]
    artist_list = [strip_punctuation(result.text.strip()) for result in soup.select(
        "div.chart-results-list > div.o-chart-results-list-row-container> ul.o-chart-results-list-row > li:nth-child("
        "4) > ul > li:nth-child(1) span")]
    position_list = [i for i in range(1, 100 + 1)]

    chart_data = [{'Position': positions, 'Artist': artists, 'Track': songs} for positions, artists, songs in
                             zip(position_list, artist_list, song_list)]

    return chart_data

def get_NZ_top_40():
    """ Gets the data from the NZTop40 website, and then creates a JSON object with all the relevant
        information """

    url = "https://nztop40.co.nz/chart/singles"
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")

    song_list_raw = soup.findAll("h2", {"class": "title"})
    song_list = []
    for element in song_list_raw:
        song_list.append(strip_punctuation(element.string))

    artist_list_raw = soup.findAll("h3", {"class": "artist"})
    artist_list = []
    for element in artist_list_raw:
        artist_list.append(strip_punctuation(element.string))

    position_list = [i for i in range(1, 100 + 1)]

    chart_data = [{'Position': positions, 'Artist': artists, 'Track': songs} for positions, artists, songs in
                             zip(position_list, artist_list, song_list)]

    return chart_data

def strip_punctuation(input_str):
    """ Spotify doesn't like special characters so best to remove punctuation """
    punctuation = '''{};:'"\,<>/@#$%^&*_~'''
    for element in input_str:
        if element in punctuation:
            if element == "&":
                input_str = input_str.replace(element, "and")
            else:
                input_str = input_str.replace(element, "")
    return input_str
