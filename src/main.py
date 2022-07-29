import getopt
import getpass, imaplib
import email
from email import parser,header
import sys
from bs4 import BeautifulSoup
from DataBaseConnect import pushToAtlas
from NotesParse import parseNotes


def decodeStr(s):
    try:
        subject = email.header.decode_header(s)
    except:
        # print('Header decode error')
        return None 
    sub_bytes = subject[0][0] 
    sub_charset = subject[0][1]

    if None == sub_charset:
        subject = sub_bytes
    elif 'unknown-8bit' == sub_charset:
        subject = str(sub_bytes, 'utf8')
    else:
        subject = str(sub_bytes, sub_charset)
    return subject

argdict = {}
def getCMDArgs(argv):
    try:
        opts, args = getopt.getopt(argv,"hu:p:s:a:",["username=","password=","server=","atlasuri="])
    except getopt.GetoptError:
        print('Usage: python3 main.py -u <username> -p <password> -s <server> -a <atlasuri>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('Usage: python3 main.py -u <username> -p <password> -s <server>')
            sys.exit(0)
        elif opt in ('-u', '--username'):
            argdict['username'] = arg
        elif opt in ('-p', '--password'):
            argdict['password'] = arg
        elif opt in ('-s', '--server'):
            argdict['server'] = arg
        elif opt in ('-a', '--atlasuri'):
            argdict['atlasuri'] = arg
        else:
            print('Usage: python3 main.py -u <username> -p <password> -s <server> -a <atlasuri>')
            sys.exit(0)

def parseContent():
    server = argdict['server']
    port = 993
    M = imaplib.IMAP4_SSL(server, port)
    username = argdict['username']
    password = argdict['password']
    M.login(username,password)
    M.select()
    typ, data = M.search(None, 'ALL')
    for num in data[0].split():
        typ, data = M.fetch(num, '(RFC822)')
        msg = parser.BytesParser().parsebytes(data[0][1])
        sub = decodeStr(msg['Subject'])
        if sub.find('的笔记') == -1:
            continue
        for part in msg.walk():
            if (part.get_content_type() == 'text/html'):
                BooksNote = part.get_payload(decode=True).decode('utf-8')
                notesList = parseNotes(BooksNote)
                pushToAtlas(notesList,argdict['atlasuri'])
        num = num.decode('utf-8')
        print(num, sub) 
    M.close()
    M.logout()

if "__main__" == __name__:
    getCMDArgs(sys.argv[1:])
    parseContent()