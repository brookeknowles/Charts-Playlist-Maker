from bs4 import BeautifulSoup
import requests
import json

url = "https://www.billboard.com/charts/hot-100/"
result = requests.get(url)
soup = BeautifulSoup(result.text, "html.parser")
soup.find("div", class_="lxml")

song_list = [result.text.strip() for result in soup.select("div.chart-results-list > div.o-chart-results-list-row-container > ul.o-chart-results-list-row > li:nth-child(4) > ul > li:nth-child(1) h3")]
artist_list = [result.text.strip() for result in soup.select("div.chart-results-list > div.o-chart-results-list-row-container> ul.o-chart-results-list-row > li:nth-child(4) > ul > li:nth-child(1) span")]

chart_data = json.dumps([{'Artist': artists, 'Track': songs} for artists, songs in zip(artist_list, song_list)])
print(chart_data)
