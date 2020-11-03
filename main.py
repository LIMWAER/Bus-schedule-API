import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import time
import json

url = "https://mybuses.ru/moscow/"
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

div = soup.find("div", class_="list-group")
print(div)