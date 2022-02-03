#!/usr/bin/env python3

from pprint import pprint
from pymarc import parse_xml_to_array

import argparse
import csv
import datetime
import glob
import itertools
import logging
import pathlib
import os
import re
import struct

import constants


def parse_008_field(data):
    print(f"data={data}")
    print(f"template={constants.FF_TEMPLATE['BOOKS']}")

    start = 0

    bib_info = {}

    for i, field_len in enumerate(constants.FF_TEMPLATE['BOOKS']):
        len = int(field_len)
        print(len)
        end = start + len
        val = data[start:end].strip()

        print(f"{start}:{end-1}")

        name = constants.FF_FIELDS['BOOKS'][i]
        print(f"bib_info[{name}]: {val}")

        bib_info[name] = val
        if name == "Lang":
            bib_info["Language"] = constants.LANG[val]

        start = end

    return bib_info


def dump(obj):
    for attr in dir(obj):
        print("obj.%s = %r" % (attr, getattr(obj, attr)))

def format_date(tstamp):
    dt = datetime.datetime.strptime(tstamp, "%Y%m%d%H%M%S.%f")
    #return dt.strftime("%Y-%m-%d %H:%M")
    return dt.strftime("%c")


def clean(buf):
    if buf:
        return buf.strip(" ,.:[]/")
    else:
        return ""

def catalog_src(record):
    return clean(record['040'].format_field())

def langcode(record):
    return clean(record['041'].format_field())

def loc_call_number(record):
    if '050' in record:
        return clean(record['050'].format_field())
    else:
        return ''

def lcl_call_number(record):
    return clean(record['099'].format_field())

def publoc(record):
    return clean(record['260']['a'])


logging.basicConfig(
    format='%(asctime)s - marc-report - %(levelname)s - %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p')

parser = argparse.ArgumentParser(
    description="Report of all MARC fields present in marcxml_in files.")
parser.add_argument("input_dir", metavar="INPUT_DIRECTORY",
    help="Input directory")
parser.add_argument("-d", "--debug",
    help="Enable debugging messages", action="store_true")
args = parser.parse_args()

if args.debug:
    logging.getLogger().setLevel(logging.DEBUG)

logging.debug("Input file: %s", args.input_dir)

marc_files = sorted(glob.glob(f"{args.input_dir}/*.xml"))

try:
    term_size = os.get_terminal_size()
    term_width = term_size.columns
except:
    term_width = 80

for marc_file in marc_files:
    logging.debug(marc_file)

for marc_file in marc_files:
    logging.debug(marc_file)
    records = parse_xml_to_array(marc_file)
    for record in records:
        logging.debug(record)
        print(dir(record))

        fields = record.get_fields()
        for field in fields:
            #print(vars(field))
            print(field)
            print(field.format_field())

        rec_id = record['001'].format_field()
        org = record['003'].format_field()

        last_trans_date = record['005'].format_field()
        fmt_date = format_date(last_trans_date)

        gen_info_str = record['008'].format_field()

        bib_info = parse_008_field(gen_info_str)

        oclc = [entry.format_field() for entry in record.get_fields('035')]

        #lccn = record['010'].format_field()

        for entry in record.get_fields('955'):
            print(dir(entry))
            for key, value in entry.subfields_as_dict().items():
                print(f"{key} {value}")
                print(f"{constants.SUBFIELDS_955[key]}: {value[0]}")

        title = clean(record.title())
        uniform_title = clean(record.title())
        author = clean(record.author())
        publisher = clean(record.publisher())
        pub_year = clean(record.pubyear())
        pub_loc = clean(publoc(record))
        isbn = clean(record.isbn())
        issn = clean(record.issn())
        issn_title = clean(record.issn_title())
        issnl = clean(record.issnl())
        location = clean(record.location())
        pos = record.pos
        leader = record.leader

        loc_call_num = loc_call_number(record)

        try:
            cat_src = catalog_src(record)
        except:
            cat_src = ""

        try:
            lang_code = langcode(record)
        except Exception as e:
            print(f"Error getting lang_code: {e}")
            lang_code = ""

        try:
            lcl_call_num = lcl_call_number(record)
        except Exception as e:
            print(f"Error getting lcl_call_num: {e}")
            lcl_call_num = ""

        notes = [entry.format_field()
            for entry in record.notes()]

        phys_desc = [entry.format_field()
            for entry in record.physicaldescription()]

        subjects = [entry.format_field()
            for entry in record.subjects()]

        series = [entry.format_field()
            for entry in record.series()]

        sudoc = clean(record.sudoc())

        print('-' * term_width)

        print(f"Library of Congress Call Number: {loc_call_num}")
        print(f"Catalog Source: {cat_src}")
        print(f"Local Call No: {lcl_call_num}")
        print(f"Language Code: {lang_code}")

        print(f"Record ID: {rec_id}")
        print(f"Oranization Code: {org}")
        print(f"008 Data:")
        for key, val in bib_info.items():
            if val and not re.search(r'^\|+$', val):
                print(f"\t{key}: '{val}'")

        print(f"OCLC Control Number: {', '.join(oclc)}")
        print(f"Last Transaction Date: {fmt_date}")
        print(f"Title: {title}")
        print(f"Uniform Title: {uniform_title}")
        print(f"Author: {author}")
        print(f"Publisher: {publisher}")
        print(f"Publication Year: {pub_year}")
        print(f"Publication Location: {pub_loc}")
        print(f"ISBN: {isbn}")
        print(f"ISSN: {issn}")
        print(f"ISSN Title: {issn_title}")
        print(f"ISSNL: {issnl}")
        print(f"Location: {location}")
        print(f"pos: {pos}")
        print(f"Leader: {leader}")
        print("Notes: {}".format(", ".join(notes)))
        print("Physical Description: {}".format(", ".join(phys_desc)))
        print("Subject: {}".format(", ".join(subjects)))
        print(f"Series: {', '.join(series)}")
        print(f"Superintendent of Documents (SuDoc): {sudoc}")
        print('-' * term_width)

