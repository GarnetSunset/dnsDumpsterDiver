from bs4 import BeautifulSoup, SoupStrainer
import requests, re

try: input = raw_input
except NameError: pass

host = input("Input the host e.g. \"google.com\"\n>")

r = requests.get("https://dnsdumpster.com/")
c = r.content

soup = BeautifulSoup(c, 'lxml')

csrf = soup.find('input').get('value')
csrf.strip()

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Origin': 'https://dnsdumpster.com',
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'https://dnsdumpster.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
}

data = {
  'csrfmiddlewaretoken': csrf,
  'targetip': host
}

cookies = {
    'csrftoken': csrf,
}

response = requests.post('https://dnsdumpster.com/', headers=headers, cookies=cookies, data=data)
c = response.content

soup = BeautifulSoup(c, 'lxml')

for link in soup.find_all('a', href=True):
    if "https://dnsdumpster.com/static/xls/" in link['href']:
        r = requests.get(link['href'], allow_redirects=True)
        open(host+'.xlsx', 'wb').write(r.content)
        r = requests.get("https://dnsdumpster.com/static/map/"+host+".png", allow_redirects=True)
        open(host+'.png', 'wb').write(r.content)
