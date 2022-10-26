import email
import getopt
import imaplib
import sys
from email import parser, header

from DataBaseConnect import push_to_atlas, push_to_atlas_my_favorite
from NotesParse import parse_notes


def decode_str(s):
    subject = email.header.decode_header(s)
    sub_bytes = subject[0][0]
    sub_charset = subject[0][1]

    if sub_charset is not None:
        subject = sub_bytes
    elif 'unknown-8bit' == sub_charset:
        subject = str(sub_bytes, 'utf8')
    else:
        subject = str(sub_bytes, 'utf8')
    return subject


arg_dict = {}


def get_cmd_args(argv):
    try:
        opts, args = getopt.getopt(argv, "hu:p:s:a:", ["username=", "password=", "server=", "atlas_uri="])
    except getopt.GetoptError:
        print('Usage: python3 main.py -u <username> -p <password> -s <server> -a <atlas_uri>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('Usage: python3 main.py -u <username> -p <password> -s <server>')
            sys.exit(0)
        elif opt in ('-u', '--username'):
            arg_dict['username'] = arg
        elif opt in ('-p', '--password'):
            arg_dict['password'] = arg
        elif opt in ('-s', '--server'):
            arg_dict['server'] = arg
        elif opt in ('-a', '--atlas_uri'):
            arg_dict['atlas_uri'] = arg
        else:
            print('Usage: python3 main.py -u <username> -p <password> -s <server> -a <atlas_uri>')
            sys.exit(0)


# noinspection PyUnresolvedReferences
def parse_content():
    res = 0
    server = arg_dict['server']
    port = 993
    m = imaplib.IMAP4_SSL(server, port)
    username = arg_dict['username']
    password = arg_dict['password']
    m.login(username, password)
    m.select()
    typ, data = m.search(None, 'UNSEEN')
    # noinspection PyUnresolvedReferences
    for num in data[0].split():
        typ, data = m.fetch(num, '(RFC822)')
        # noinspection PyUnresolvedReferences
        msg = parser.BytesParser().parsebytes(data[0][1])
        sub = decode_str(msg['Subject']).strip()
        if sub.find('的笔记') == -1:
            continue
        for part in msg.walk():
            if part.get_content_type() == 'text/html':
                books_note = part.get_payload(decode=True).decode('utf-8')
                notes_list, favorite_notes = parse_notes(books_note)
                push_to_atlas(notes_list, arg_dict['atlas_uri'])
                push_to_atlas_my_favorite(favorite_notes, arg_dict['atlas_uri'])
        res += 1
        print("获取图书" + str(res) + " " + sub)
        m.store(num, '+FLAGS', '\\Seen')
    m.close()
    m.logout()
    return res


if "__main__" == __name__:
    get_cmd_args(sys.argv[1:])
    cnt = parse_content()
