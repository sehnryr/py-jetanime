from jetanime import getList
from output import animeList
import difflib

search = str(input('Enter search : '))

def similarity(word, pattern):
    return difflib.SequenceMatcher(a=word.lower(), b=pattern.lower()).ratio()

threshold = 0.3

for anime in animeList():
    for word in search.split():
        if similarity(word, anime) > threshold:
            print(anime)

#for anime in _list:
#    for word in text.split():
#        if similarity(word, lookup) > threshold:
#            print(word)