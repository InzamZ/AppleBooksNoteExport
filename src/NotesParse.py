import re

from bs4 import BeautifulSoup


def parse_notes(html):
    notes_list = []
    favorite_notes = []
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup.prettify())
    book_name = soup.find('h1', class_="booktitle").text.strip()
    author = soup.find('h2').text.strip()
    notes = soup.find_all('div', class_='annotation')
    for x in notes:
        item = {"from": book_name, "author": author, "content": x.find(
            'p', class_='annotationrepresentativetext').text.strip(), "chapter": x.find(
            'div', class_='annotationchapter').text.strip(),
                "date": x.find('div', class_='annotationdate').text.strip(),
                "note": x.find('p', class_='annotationnote').text.strip()}
        if x.find('div', class_='annotationselectionMarker defaultColor') is not None:
            item["type"] = 0
        elif x.find('div', class_='annotationselectionMarker yellow') is not None:
            item["type"] = 1
        elif x.find('div', class_='annotationselectionMarker green') is not None:
            item["type"] = 2
        elif x.find('div', class_='annotationselectionMarker blue') is not None:
            item["type"] = 3
        elif x.find('div', class_='annotationselectionMarker pink') is not None:
            item["type"] = 4
        elif x.find('div', class_='annotationselectionMarker purple') is not None:
            item["type"] = 5
        if item["content"].strip() == "":
            continue
        item = parse_note_args(item)
        pattern = '^[^\u4e00-\u9fa5A-Za-z]+'
        res = re.match(pattern, item["chapter"])
        if res:
            item["chapter"] = item["chapter"][len(res.group(0)):]
        if item["type"] == 0:
            favorite_notes.append(item)
        notes_list.append(item)
    return notes_list, favorite_notes


def parse_note_args(item):
    comment = item["note"]
    comment = comment.splitlines()
    note_res = ""
    pattern = '\\[\\[[a-zA-Z]+\\]\\]'
    for x in comment:
        res = re.match(pattern, x)
        if res:
            the_key = res.group(0)[2:-2]
            item[the_key] = x[len(res.group(0)):]
        else:
            note_res += x
    item["note"] = note_res
    return item


if "__main__" == __name__:
    f = open('./test/BooksNote.html', 'r')
    notesList, favoriteNotes = parse_notes(f.read())
    print(notesList)
    print(favoriteNotes)
    # item = {"from": "", "author": "", "content": "", "chapter": "", "date": "", "note": "[[speaker]]me\nhello", "type": 0}
    # parse_note_args(item)
