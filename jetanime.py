from requests_html import HTMLSession
import re
from unidecode import unidecode
from urllib.parse import urljoin, urlparse

global jetanime_url
jetanime_url = 'https://www.jetanime.cc'

class vid:
    def __init__(self, url):

        def vosta(arg):
            lang = 'VOSTFR'
            if arg.find('VOSTA') >= 0:
                arg = arg.replace(' (VOSTA)', '')
                lang = 'VOSTA'
            return arg, lang

        url = urljoin('https://www.jetanime.cc', url)
        session = HTMLSession()
        r = session.get(url)
        soup = r.html.xpath("//div[@role='tablist']")
        sauce = soup[0].xpath("//div[@class='panel panel-default']")
        for s in sauce:
            category = unidecode(s.text).split(':\n', 1)[0]
            vegetables = s.find('a')
            temp = list()
            self.films = None
            if category.lower() == 'films':
                for vegetable in vegetables:
                    link = vegetable.attrs['href']
                    leaf = unidecode(vegetable.text)
                    foliage = leaf.split(': ', 1)
                    if len(foliage) > 1:
                        number = foliage[0].replace('Film ', '')
                        name = foliage[1]
                    else:
                        name = foliage[0]
                        number = name.replace('Film ', '')
                    spices = name.split(' ')
                    for idx, spice in enumerate(spices):
                        spices[idx] = spice.capitalize()
                    name = ' '.join(spices)
                    fruits = vosta(name)
                    number = fruits[0]
                    lang = fruits[1]
                    temp.append((number, [name, link, lang]))
                temp.reverse()
                temp = dict(temp)
                self.films = temp
            self.episodes = None
            if category.lower() == 'episodes':
                for vegetable in vegetables:
                    link = vegetable.attrs['href']
                    number = unidecode(vegetable.text).replace('Episode ', '')
                    fruits = vosta(number)
                    number = fruits[0]
                    lang = fruits[1]
                    temp.append((number, [link, lang]))
                temp.reverse()
                temp = dict(temp)
                self.episodes = temp
            self.list = [self.films, self.episodes]

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

# def getAnimeList1():

#     def deCFEmail(fp):
#         r = int(fp[:2],16)
#         email = ''.join([chr(int(fp[i:i+2], 16) ^ r) for i in range(2, len(fp), 2)])
#         return email

#     session = HTMLSession()
#     r = session.get(jetanime_url)
#     soup = r.html.xpath("//select[@id='liste_animes']")
#     sauce = soup[0].xpath("//option")
#     animes = list()
#     for anime in sauce:
#         link = anime.attrs['value']
#         email = anime.xpath("//template")
#         name = unidecode(anime.text)
#         if email:
#             email = unidecode(deCFEmail(email[0].attrs['data-cfemail']))
#             name = name.replace('[email protected]', email).replace('\n', ' ')
#         animes.append((name, link))
#     return dict(animes)

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

class getLen:
    def __init__(self, url):
        v = vid(url)
        eps = v.episodes
        if eps is not None:
            self.episodesLen = len(eps)
        else:
            self.episodesLen = 0
        fms = v.films
        if fms is not None:
            self.filmsLen = len(fms)
        else:
            self.filmsLen = 0

def lastAnimeUpdate():
    session = HTMLSession()
    r = session.get(url)
    soup = r.html.xpath("//div[@id='last_animes']")
    sauce = soup[0].xpath("//a")
    animes = list()
    for spice in sauce:
        name = unidecode(spice.text)
        link = spice.attrs['href']
        animes.append((name, link))
    return dict(animes)