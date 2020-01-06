from jetanime import getList, getEpList, getGounLimitedUrl, getTitle
from lib import download, sizeFile

# Search for anime :
search = str(input('Enter search : '))

_list = getList()

matching = []
for content in _list:
  if search.lower() in content.lower():
    matching.append(content)
    matching.sort()

if matching:
    for idx, content in enumerate(matching):
        print(f"{idx + 1} : {content}")
    print(f"{idx + 2} : Cancel")
else:
    print("No result found :/")
    exit()

#Select precise anime :
choice = str(input('> '))
if not choice or choice >= f"{idx + 2}":
    exit()
choice = matching[int(choice)-1]

url = str(_list[choice])
_list = getEpList(url)

_list1 = []
for content in _list:
    _list1.append(_list[content])

for idx, content in enumerate(_list):
    print(f"{idx + 1} : {content}")
print(f"{idx + 2} : Cancel")

#Select episode:
choice = int(input('> '))
if not choice or choice == f"{idx + 2}":
    exit()

url = str(_list1[choice - 1])
link = getGounLimitedUrl(url)
name = getTitle(url)

fileext = link.split('/')

print(f'[*] Downloading file of size {sizeFile(link)} B...')
download(link, f"{name}{str(fileext[-1])[-4:]}")