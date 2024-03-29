import pathlib
import re

def get_lang(lang_file):
    lang = {}
    with open(lang_file) as f:
        lines = f.readlines()
        for line in lines:
            cols = line.strip().split('|')
            lang[cols[0]] = cols[3]
    return lang

def get_marc_tag(tag_file):
    tag = {}
    with open(tag_file) as f:
        lines = f.readlines()
        for line in lines:
            num, desc = line.strip().split(',', 1)
            desc = re.sub(r'\s*\(N?R\)$', '', desc)
            tag[num] = desc
    return tag

# wget https://www.loc.gov/standards/iso639-2/ISO-639-2_utf-8.txt
LANG_FILE = pathlib.Path(__file__).parent / "ISO-639-2_utf-8.txt"

# ./gen-marc-tag-list.py  > tags.csv
MARC_TAG_FILE = pathlib.Path(__file__).parent / "marc-tags.csv"

LANG = get_lang(LANG_FILE)

MARC_TAG = get_marc_tag(MARC_TAG_FILE)

# Based on https://metacpan.org/pod/MARC Perl module
FF_FIELDS = {
    'BOOKS':
        'Entered DateType Date1 Date2 Ctry Ills Audn Form Cont ' \
        'GPub Conf Fest Indx Undef1 Fict Biog Lang MRec Srce'.split(),
    'COMPUTER_FILES':
        'Entered DateType Date1 Date2 Ctry Undef1 Audn Undef2 ' \
        'File Undef3 GPub Undef4 Lang MRec Srce'.split(),
    'MAPS':
        'Entered DateType Date1 Date2 Ctry Relf Proj Prme CrTp ' \
        'Undef1 GPub Undef2 Indx Undef3 SpFm Lang MRec Srce'.split(),
    'MUSIC':
        'Entered DateType Date1 Date2 Ctry Comp FMus Undef1 Audn ' \
        'Form AccM LTxt Undef2 Lang MRec Srce'.split(),
    'SERIALS':
        'Entered DateType Date1 Date2 Ctry Freq Regl ISSN SrTp Orig ' \
        'Form EntW Cont GPub Conf Undef1 Alph S_L Lang MRec Srce'.split(),
    'VIS':
        'Entered DateType Date1 Date2 Ctry Time Undef1 ' \
        'Audn AccM GPub Undef2 TMat Tech Lang MRec Srce'.split(),
    'MIX':
        'Entered DateType Date1 Date2 ' \
        'Ctry Undef1 Form Undef2 Lang MRec Srce'.split()
}

FF_TEMPLATE = {
    'BOOKS'          : "6144341141111111311",
    'COMPUTER_FILES' : "614434131116311",
    'MAPS'           : "614434211212112311",
    'MUSIC'          : "6144321111623311",
    'SERIALS'        : "614431111111311311311",
    'VIS'            : "6144331151411311",
    'MIX'            : "614435111311"
}

SUBFIELDS_955 = {
    'a': 'Tracking information (R)',
    'b': 'IBC/BBC processing (R)',
    'c': 'Descriptive cataloging (R)',
    'd': 'Subject cataloging (R)',
    'e': 'Shelflisting and ordinary end-stage processing (R)',
    'f': 'CIP verification (R)',
    'g': 'Serials end-stage processing (R)',
    'h': 'Minimal level cataloging (MLC) (R)',
    'i': 'Whole item cataloging (R)',
    'j': 'ISSN pre-publication assignment (R)',
    'k': 'ISSN post-publication assignment (R)',
    'l': 'Holdings conversion and inventory (R)',
    'm': 'Bibliographic record cancellations (R)',
    'n': 'ISSN pre-publication elements updated (R)',
    't': 'Added copy (R)',
    'w': 'Dewey Decimal Classification (R)',
    'v': 'Enumeration and chronology'
}

