from requests_html import HTMLSession
import re
from unidecode import unidecode
from urllib.parse import urljoin, urlparse

global jetanime_url
jetanime_url = 'https://www.jetanime.cc'

class vid:
    def __init__(self, url):
        url = urljoin(jetanime_url, url)
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

def getAnimeList():
    session = HTMLSession()
    r = session.get(jetanime_url)
    soup = r.html.find('body', first=True)
    options = soup.find('option')

    animes = []
    for option in options:
        name = unidecode(option.text).replace("\n[email protected]\n", '@')
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

def getNum(url):
    url = urlparse(url)
    v = vid(url.geturl())
    number = str()
    while True:
        try:
            _dict = v.getEpisodeList()
            inverted_dict = dict()
            for key, value in _dict.items():
                inverted_dict.setdefault(value, list()).append(key)
            for num in inverted_dict[url.path]:
                number += f"{num}-"
            return number[:-1]
        except KeyError:
            _dict = v.getFilmList()
            inverted_dict = dict()
            for key, value in _dict.items():
                inverted_dict.setdefault(value[1], list()).append(key)
            for num in inverted_dict[url.path]:
                number += f"{num}-"
            return number[:-1]

def getVideoUrl(url):
    url = urljoin(jetanime_url, url)

    session = HTMLSession()
    r = session.get(url)
    r.html.render()
    soup = r.html.find('body', first=True)
    iframe = soup.find('iframe')
    url = urlparse(dict(iframe[0].attrs)['src'])
    if str(url.netloc).find('gounlimited') >= 0:
        session = HTMLSession()
        r = session.get(url.geturl())
        soup = r.html.find('body', first=True)
        while True:
            try:
                sauce = soup.find('script')
                if sauce:
                    for spice in sauce:
                        for key in dict(spice.attrs):
                            if key == 'type':
                                if len(dict(spice.attrs)) == 1:
                                    temp = str(spice.text).split('|')
                                    url = f"{url.scheme}://{temp[-5]}.{url.netloc}/{temp[-6]}/v.{temp[-7]}"
                                    return url
                else:
                    url = 'NULL'
                    return url
            except AttributeError:
                url = 'NULL'
                return url