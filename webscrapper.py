import requests
from bs4 import BeautifulSoup
import os

path = os.getcwd()


def month_converter(m):
    if m == 'january':
        return 1
    elif m == 'february':
        return 2
    elif m == 'march':
        return 3
    elif m == 'april':
        return 4
    elif m == 'may':
        return 5
    elif m == 'june':
        return 6
    elif m == 'july':
        return 7
    elif m == 'august':
        return 8
    elif m == 'september':
        return 9
    elif m == 'october':
        return 10
    elif m == 'november':
        return 11
    else:
        return 12


def month_finder(m1, y1, m2, y2):
    s = [m1, y1]
    e = [m2, y2]
    r = [s]
    if s != e:
        if y1 != y2:
            r += [[i, y1] for i in range(m1 + 1, 13)]
            for i in range(y1 + 1, y2):
                r += [[j, i] for j in range(1, 13)]
            r += [[i, y2] for i in range(1, m2 + 1)]
        else:
            r += [[i, y1] for i in range(m1 + 1, m2 + 1)]
    return r


def for_one_month(m, y, author):
    response = requests.get(f'http://explosm.net/comics/archive/{y}/{m}/{author}')
    soup = BeautifulSoup(response.content, 'html5lib')
    comics_author = soup.find('div', attrs={'class': 'small-7 medium-8 large-8 columns'})
    comics = comics_author.find_all('div', attrs={'class': "small-12 medium-12 large-12 columns"})
    comic_links = []
    comic_dates = []
    for comic in comics:
        code = comic.a['href']
        comic_date = comic.find('div', attrs={'id': 'comic-author'}).text.split()[0]
        comic_dates.append(comic_date)
        comic_links.append(f'http://explosm.net{code}')
    return comic_links, comic_dates


def each_link_finder(link):
    respo = requests.get(link)
    comic_site = BeautifulSoup(respo.content, 'html5lib')
    comic_image_link = comic_site.find('section', attrs={'id': 'comic-area'}).img['src']
    return comic_image_link


def saver(links, dates, author, path, m, y):
    e = path
    e += f'/{y}/{m}'
    if not os.path.isdir(e):
        try:
            os.makedirs(e)
        except OSError:
            print("Creation of the directory %s failed" % e)
        else:
            print("Successfully created the directory %s " % e)
    for i in range(len(links)):
        response = requests.get(f'http:{links[i]}')
        file = open(f"{e}/{dates[i]}-{author}.png", "wb")
        file.write(response.content)
        file.close()


#######__DRIVER__CODE__########
file = open('input.txt', 'r')
x = file.readlines()
file.close()
Authors = x[2].split()
for i in Authors:
    i = i.lower()
firstdate = x[0].split()
lastdate = x[1].split()
list_of_months = month_finder(month_converter(firstdate[0]), int(firstdate[1]), month_converter(lastdate[0]),
                              int(lastdate[1]))
for month in list_of_months:
    for author in Authors:
        k = for_one_month(month[0], month[1], author)
        l = []
        for i in k[0]:
            l.append(each_link_finder(i))
        saver(l, k[1], author, path, month[0], month[1])
