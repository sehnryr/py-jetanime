import sys
import requests
import curses
import locale
locale.setlocale(locale.LC_ALL,"")

def download(url, filename):
    with open(filename, 'wb') as f:
        response = requests.get(url, stream=True)
        total = response.headers.get('content-length')

        if total is None:
            f.write(response.content)
        else:
            downloaded = 0
            total = int(total)
            for data in response.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
                downloaded += len(data)
                f.write(data)
                done = int(50*downloaded/total)
                sys.stdout.write('\r[{}{}]'.format('█' * done, '.' * (50-done)))
                sys.stdout.flush()
    sys.stdout.write('\n')

def sizeFile(url):
    r = requests.head(url)

    return f"{int(r.headers['Content-Length']):n}"

def line(arg):
    line = ''
    for _ in range(len(arg) + 2):
        line += '-'
    line = f"{line}\n"
    return line

def searching(arg):
    screen = curses.initscr()
    screen.addstr(f"{arg}")
    screen.refresh()
    curses.noecho()
    search = ''
    while True:
        key_input = screen.getch()
        if key_input == 10:
            break
        elif key_input == 8:
            screen.clear()
            search = search[:-1]
            screen.addstr(f"{arg}{search}")
        else:
            screen.clear()
            search += chr(key_input)
            screen.addstr(f"{arg}{search}")
            
    screen.clear()
    curses.endwin()

    return search

def enumerates(arg):
    animes = ''
    for idx, match in enumerate(arg):
        animes += f"{idx + 1} : {match}\n"
    animes += f"{idx + 2} : Cancel\n"
    return animes

def match(_list, search):
    matching = []
    for content in _list:
        if search.lower() in content.lower():
            matching.append(content)
            matching.sort()
    return matching