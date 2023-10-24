import requests
from bs4 import BeautifulSoup as BS

def read_web_pages():
    r = requests.get("https://webscraper.io/test-sites/e-commerce/allinone")
    soup = BS(r.content)

    with open("mail/web.txt", "w") as file:
        file.write(str(soup))

