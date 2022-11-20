import email
import getopt
import imaplib
import sys
import argparse
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


def parse_cmd_args(argv):
    args_parser = argparse.ArgumentParser(description='Parse Apple Books Notes')
    args_parser.add_argument('-s', '--server', help='IMAP server', required=True)
    args_parser.add_argument('-u', '--username', help='IMAP username', required=True)
    args_parser.add_argument('-p', '--password', help='IMAP password', required=True)
    args_parser.add_argument('-a', '--atlas_uri', help='Atlas URI', required=True)
    args_parser.add_argument('-v', '--ios_version', help='IOS Version', required=True)
    return args_parser.parse_args(argv)


def parse_content(args):
    server = args.server
    username = args.username
    password = args.password
    atlas_uri = args.atlas_uri
    res = 0
    port = 993
    m = imaplib.IMAP4_SSL(server, port)
    m.login(username, password)
    m.select()
    typ, data = m.search(None, 'UNSEEN')
    for num in data[0].split():
        typ, data = m.fetch(num, '(RFC822)')
        msg = parser.BytesParser().parsebytes(data[0][1])
        sub = decode_str(msg['Subject']).strip()
        if sub.find('的笔记') == -1:
            continue
        for part in msg.walk():
            if part.get_content_type() == 'text/html':
                books_note = part.get_payload(decode=True).decode('utf-8')
                notes_list, favorite_notes = parse_notes(books_note)
                push_to_atlas(notes_list, atlas_uri)
                push_to_atlas_my_favorite(favorite_notes, atlas_uri)
        res += 1
        print("获取图书" + str(res) + " " + sub)
        m.store(num, '+FLAGS', '\\Seen')
    m.close()
    m.logout()
    return res


def main():
    args = parse_cmd_args(sys.argv[1:])
    parse_content(args)


if "__main__" == __name__:
    main()
