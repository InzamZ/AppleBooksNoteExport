import enum
from bs4 import BeautifulSoup


def parseNotes(html):
    notesList = []
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup.prettify())
    bookName = soup.find('h1', class_="booktitle").text.strip()
    author = soup.find('h2').text.strip()
    notes = soup.find_all('div', class_='annotation')
    for x in notes:
        item = {"from": bookName, "author": author}
        item["content"] = x.find('p', class_ = 'annotationrepresentativetext').text.strip()
        item["chapter"] = x.find('div', class_ = 'annotationchapter').text.strip()
        item["date"] = x.find('div', class_ = 'annotationdate').text.strip()
        item["note"] = x.find('p', class_ = 'annotationnote').text.strip()
        if x.find('div' , class_ ='annotationselectionMarker defaultColor') != None:
            item["type"] = 0
        else :
            item["type"] = 1
        notesList.append(item)
    return notesList

if "__main__" == __name__:
    f = open('BooksNote.html', 'r')
    notesList = parseNotes(f.read())
    print(notesList)
