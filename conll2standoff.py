#!/usr/bin/env python
# coding: utf8


"""
Convert CoNLL to BioNLP standoff.

Accept IO, IOB, and IOBES tags.
Be graceful about tag-sequence errors.

Input needs at least 4 tab-separated columns:
    token, start offset, end offset, tag [, more...]
"""


from __future__ import unicode_literals


import sys
import codecs

from document import Document


def main():
    '''
    Run as script.
    '''
    conll2standoff(codecs.getreader('utf8')(sys.stdin),
                   codecs.getwriter('utf8')(sys.stdout))


def conll2standoff(src, tgt):
    """Convert CoNLL with character offsets to BioNLP standoff."""
    rows = parse_conll(src)
    rows = reformat(rows)
    text = '\n'.join('\t'.join(r) for r in rows) + '\n'
    doc = Document.from_nersuite(text)
    tgt.write(doc.to_standoff())


def parse_conll(lines):
    """Parse CoNLL TSV."""
    for line in lines:
        if not line.lower().startswith('# doc_id'):
            line = line.rstrip()
            if line:
                yield line.split('\t')
            else:
                yield []


def reformat(rows):
    """Reformat CoNLL input to well-formed NERSuite format."""
    last = OUTSIDE[0]
    for row in rows:
        if not row:
            last = OUTSIDE[0]
        else:
            # Flip token/tag and sanitise the tag sequence.
            tag = row[3]
            tag = last = fix_tag(tag, last)
            row[3] = row[0]
            row[0] = tag
        yield row


OUTSIDE = ('O', 'O-NIL')
INSIDE = ('I', 'E')
BEGIN = ('B', 'S')


def fix_tag(tag, last):
    """Ensure a valid IOB sequence."""
    if tag in OUTSIDE:
        tag = OUTSIDE[0]
    else:
        # Definitely use B or I, including something like "O-chemical".
        tag, label = tag[0], tag[1:]
        if tag in BEGIN or last in OUTSIDE or last[1:] != label:
            tag = BEGIN[0]
        else:
            tag = INSIDE[0]
        tag += label  # rejoin
    return tag


if __name__ == '__main__':
    main()
