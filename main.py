from bs4 import BeautifulSoup
import requests
import json

# Gets the data from the Billboard Hot 100 website, and then creates a JSON object with all the relevant information

url = "https://www.billboard.com/charts/hot-100/"
result = requests.get(url)
soup = BeautifulSoup(result.text, "html.parser")
soup.find("div", class_="lxml")

song_list = [result.text.strip() for result in soup.select("div.chart-results-list > div.o-chart-results-list-row-container > ul.o-chart-results-list-row > li:nth-child(4) > ul > li:nth-child(1) h3")]
artist_list = [result.text.strip() for result in soup.select("div.chart-results-list > div.o-chart-results-list-row-container> ul.o-chart-results-list-row > li:nth-child(4) > ul > li:nth-child(1) span")]
position_list = [i for i in range(1, 100 + 1)]

chart_data = json.dumps([{'Position': positions, 'Artist': artists, 'Track': songs} for positions, artists, songs in zip(position_list, artist_list, song_list)])

print(json.dumps(json.loads(chart_data), indent=3))
