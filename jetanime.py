from requests_html import HTMLSession
import re
import unidecode
from urllib.parse import urljoin

class Jetanime():
    def __init__(self):
        session = HTMLSession()
        self.url = 'https://www.jetanime.cc'
        self.r = session.get(self.url)
        self.r.html.render()
        self.soup = self.r.html.find('body', first=True)

    def getList(self):

        options = self.soup.find('option')

        animes = []
        for option in options:
            name = unidecode.unidecode(option.text)
            url = urljoin(self.url, option.attrs['value'])
            animes.append((name, url))

        return dict(animes)
    
def getTitle(url):
    session = HTMLSession()
    r = session.get(url)
    r.html.render()
    soup = r.html.find('body', first=True)
    
    title = soup.find('div')
    for t in title:
        if 'col-md-12' in str(t.attrs):
            break
    return t.text
    
def getEpList(url):
    session = HTMLSession()
    r = session.get(url)
    r.html.render()
    soup = r.html.find('body', first=True)
    lines = soup.find('div')
    episodes = []
    for line in lines:
        if 'sec-0' in str(line.attrs):
            for l in line.find('a'):
                name = unidecode.unidecode(l.text)
                url = urljoin(url, l.attrs['href'])
                episodes.append((name, url))
            break

    episodes.reverse()
    return dict(episodes)

def getGounLimitedUrl(url):
    session = HTMLSession()
    r = session.get(url)
    r.html.render()
    soup = r.html.find('body', first=True)
    a = soup.find('p')

    def Find(string): 
        search = 'http[s]?:\/\/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        url = re.findall(search, string) 
        return url 

    for i in a:
        if 'iframe' in str(i.html):
            link = str(i.html)
            result = Find(link)
    
    url = result[0]
    session = HTMLSession()
    r = session.get(url)
    soup = r.html.find('script')
    for i in soup:
        if 'mp4' in str(i.html):
            sauce = str(i.html)
            break
    sauce_string = sauce.split('|')
    link = f"https://{sauce_string[-5]}.gounlimited.to/{sauce_string[-6]}/v.mp4"
    return link