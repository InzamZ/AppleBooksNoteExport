from ast import parse, pattern
import enum
from pickle import NONE
import re
from bs4 import BeautifulSoup


def parseNotes(html):
    notesList = []
    favoriteNotes = []
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup.prettify())
    bookName = soup.find('h1', class_="booktitle").text.strip()
    author = soup.find('h2').text.strip()
    notes = soup.find_all('div', class_='annotation')
    for x in notes:
        item = {"from": bookName, "author": author}
        item["content"] = x.find(
            'p', class_='annotationrepresentativetext').text.strip()
        item["chapter"] = x.find(
            'div', class_='annotationchapter').text.strip()
        item["date"] = x.find('div', class_='annotationdate').text.strip()
        item["note"] = x.find('p', class_='annotationnote').text.strip()
        if x.find('div', class_='annotationselectionMarker defaultColor') != None:
            item["type"] = 0
        elif x.find('div', class_='annotationselectionMarker yellow') != None:
            item["type"] = 1
        elif x.find('div', class_='annotationselectionMarker green') != None:
            item["type"] = 2
        elif x.find('div', class_='annotationselectionMarker blue') != None:
            item["type"] = 3
        elif x.find('div', class_='annotationselectionMarker pink') != None:
            item["type"] = 4
        elif x.find('div', class_='annotationselectionMarker purple') != None:
            item["type"] = 5
        if (item["content"].strip() == ""):
            continue
        item = parseNoteArgs(item)
        if item["type"] == 0:
            favoriteNotes.append(item)
        notesList.append(item)
    return notesList, favoriteNotes


def parseNoteArgs(item):
    comment = item["note"]
    comment = comment.splitlines()
    noteRes = ""
    pattern = '\[\[[a-zA-Z]+\]\]'
    for x in comment:
        res = re.match(pattern, x)
        if res:
            theKey = res.group(0)[2:-2]
            item[theKey] = x[len(res.group(0)):]
        else:
            noteRes += x
    item["note"] = noteRes
    return item

if "__main__" == __name__:
    f = open('./test/BooksNote.html', 'r')
    notesList, favoriteNotes = parseNotes(f.read())
    print(notesList)
    print(favoriteNotes)
    # item = {"from": "", "author": "", "content": "", "chapter": "", "date": "", "note": "[[speaker]]me\nhello", "type": 0}
    # parseNoteArgs(item)