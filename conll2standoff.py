#!/usr/bin/env python
# coding: utf8


from __future__ import unicode_literals


import sys

from document import Document


def main():
    '''
    Run as script.
    '''
    text = ''
    for line in sys.stdin:
        # Decode and flip token and tag.
        line = line.decode('utf8')
        if not line.isspace():
            token, start, end, tag = line.rstrip().split('\t')
            if tag.startswith('O') and tag not in ('O', 'O-NIL'):
                tag = 'I' + tag[1:]
            line = '{}\t{}\t{}\t{}\n'.format(tag, start, end, token)
        text += line

    doc = Document.from_nersuite(text)
    sys.stdout.write(doc.to_standoff().encode('utf8'))


if __name__ == '__main__':
    main()
