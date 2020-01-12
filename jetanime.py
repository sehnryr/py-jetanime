from requests_html import HTMLSession
import re
from unidecode import unidecode
from urllib.parse import urljoin, urlparse

global jetanime_url
jetanime_url = 'https://www.jetanime.cc'

class vid:
    def __init__(self, url):
        url = urljoin('https://www.jetanime.cc', url)
        session = HTMLSession()
        r = session.get(url)
        soup = r.html.find('body', first=True)
        lines = soup.find('div')
        self.list = list()
        self.films = list()
        self.episodes = list()
        for line in lines:
            attributes = line.attrs
            try:
                if attributes['role'] == 'tablist':
                    cat = line.find('div')
                    for c in cat:
                        attributes = c.attrs
                        try:
                            if attributes['class'] == ('panel', 'panel-default'):
                                sec = c.find('div')
                                for s in sec:
                                    _s = s.attrs
                                    try:
                                        if str(_s['id']).find('sec-') >= 0:
                                            soup = s.find('a')
                                            temp_film = list()
                                            temp_episode = list()
                                            for sauce in soup:
                                                num = unidecode(sauce.text)
                                                link = sauce.attrs['href']
                                                lang = 'VOSTFR'
                                                if num.find('(VOSTA)') >= 0:
                                                    num = num.replace(' (VOSTA)', '')
                                                    lang = 'VOSTA'
                                                for s in sec:
                                                    _s = s.attrs
                                                    try:
                                                        if str(_s['class']).find('panel-title') >= 0:
                                                            search = unidecode(s.text)
                                                            if search.find('Film') >= 0:
                                                                if num.find(':') >= 0:
                                                                    _list = num.split(': ', 1)
                                                                    num = _list[0].replace('Film ', '')
                                                                    name = _list[1]
                                                                    temp_film.append((num, [link, name, lang]))
                                                                else:
                                                                    num = num.replace('Film ', '')
                                                                    temp_film.append((num, [link, lang]))
                                                                
                                                            if search.find('Episode') >= 0:
                                                                num = num.replace('Episode ', '')
                                                                if num.find('-') >= 0:
                                                                    _list = num.split('-')
                                                                    _list.reverse()
                                                                    for num in _list:
                                                                        temp_episode.append((num, [link, lang]))
                                                                else:
                                                                    temp_episode.append((num, [link, lang]))
                                                    except KeyError:
                                                        pass
                                            if temp_film:
                                                self.films.append(temp_film)
                                            if temp_episode:
                                                self.episodes.append(temp_episode)
                                    except KeyError:
                                        pass
                        except KeyError:
                            pass
            except KeyError:
                pass

        for idx, film in enumerate(self.films):
            film.reverse()
            self.films[idx] = dict(film)
        try:
            self.films = self.films[0]
        except IndexError:
            self.films = None

        for idx, episode in enumerate(self.episodes):
            episode.reverse()
            self.episodes[idx] = dict(episode)
        try:
            self.episodes = self.episodes[0]
        except IndexError:
            self.episodes = None

def getAnimeList():
    session = HTMLSession()
    r = session.get(jetanime_url)
    soup = r.html.find('body', first=True)
    options = soup.find('option')

    def deCFEmail(fp):
        r = int(fp[:2],16)
        email = ''.join([chr(int(fp[i:i+2], 16) ^ r) for i in range(2, len(fp), 2)])
        return email

    animes = []
    for option in options:
        decoded = str()
        temp = option.find('template')
        if temp:
            temps = temp[0].attrs
            for tp in temps:
                if tp == 'data-cfemail':
                    decoded = deCFEmail(temps[tp])
                    break

        name = unidecode(option.text).replace('[email protected]', decoded).replace('\n', ' ')
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
    try:
        _dict = v.episodes
        inverted_dict = dict()
        for key, value in _dict.items():
            inverted_dict.setdefault(value, list()).append(key)
        for num in inverted_dict[url.path]:
            number += f"{num}-"
        return number[:-1]
    except KeyError:
        _dict = v.films
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