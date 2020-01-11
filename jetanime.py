from requests_html import HTMLSession
import re
from unidecode import unidecode
from urllib.parse import urljoin, urlparse

global jetanime_url
jetanime_url = 'https://www.jetanime.cc'

def getAnimeList():
    session = HTMLSession()
    r = session.get(jetanime_url)
    soup = r.html.find('body', first=True)
    options = soup.find('option')

    animes = []
    for option in options:
        name = unidecode(option.text)
        url = option.attrs['value']
        animes.append((name, url))

    return dict(animes)

def getAnimeName(url):
    url = urlparse(url)
    if str(url.path).startswith('/anime') == True:
        _dict = getAnimeList()
        inverted_dict = dict()
        for key, value in _dict.items():
            inverted_dict.setdefault(value, list()).append(key)

        return inverted_dict[url.path]
    else:
        session = HTMLSession()
        r = session.get(url.geturl())
        soup = r.html.find('body', first=True)
        ul = soup.find('ul')
        for u in ul:
            for c in dict(u.attrs):
                if c == 'class':
                    if list(dict(u.attrs)[c])[0] == 'breadcrumb':
                        temp = u.find('li')
                        return unidecode(temp[1].text)

def getGounLimitedUrl(url):
    session = HTMLSession()
    r = session.get(url)
    r.html.render()
    soup = r.html.find('body', first=True)
    a = soup.find('p')

    def Find(string): 
        url = re.findall(r'http[s]?:\/\/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string) 
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

class vid:
    def __init__(self, url):
        session = HTMLSession()
        r = session.get(url)
        soup = r.html.find('body', first=True)
        lines = soup.find('div')
        episodes = []
        for line in lines:
            _list = line.attrs
            for key in _list:
                if key == 'id':
                    if str(_list['id']).find('collapsecategory') == 0:
                        temp = []
                        search = line.find('a')
                        for s in search:
                            num = unidecode(s.text).replace('Episode ', '')
                            link = dict(s.attrs)['href']
                            if num.find(':') >= 0:
                                nums = num.split(': ')
                                number = nums[0].replace('Film ', '')
                                name = nums[1]
                                temp.append((number, [name, link]))
                            elif num.find('-') >= 0:
                                nums = num.split('-')
                                nums.reverse()
                                for num in nums:
                                    temp.append((num, link))
                            else:
                                temp.append((num, link))
                        temp.reverse()
                        episodes.append(temp)
        episodes.reverse()
        for idx, content in enumerate(episodes):
            episodes[idx] = dict(content)
        self.episodes = episodes

    def getEpisodeList(self):
        return self.episodes[0]

    def getFilmList(self):
        if len(self.episodes) > 1:
            return self.episodes[1]