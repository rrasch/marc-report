#!/usr/bin/env python3

from pprint import pprint
from pymarc import parse_xml_to_array

import argparse
import csv
import datetime
import glob
import logging
import os

def dump(obj):
    for attr in dir(obj):
        print("obj.%s = %r" % (attr, getattr(obj, attr)))

def format_date(tstamp):
    dt = datetime.datetime.strptime(tstamp, "%Y%m%d%H%M%S.%f")
    #return dt.strftime("%Y-%m-%d %H:%M")
    return dt.strftime("%c")

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

term_size = os.get_terminal_size()

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

        oclc = [entry.format_field() for entry in record.get_fields('035')]

        title = record.title() or ""
        uniform_title = record.title() or ""
        author = record.author() or ""
        publisher = record.publisher() or ""
        pub_year = record.pubyear() or ""
        isbn = record.isbn() or ""
        issn = record.issn() or ""
        issn_title = record.issn_title() or ""
        issnl = record.issnl() or ""
        location = record.location() or ""
        pos = record.pos
        leader = record.leader
        notes = [entry.format_field() for entry in record.notes()]
        phys_desc = [entry.format_field()
            for entry in record.physicaldescription()]
        subjects = [entry.format_field() for entry in record.subjects()]

        series = record.series()

        sudoc = record.sudoc() or ""

        #record.parse_leader()


        print('-' * term_size.columns)
        print(f"Record ID: {rec_id}")
        print(f"Oranization Code: {org}")
        print(f"OCLC Control Number: {', '.join(oclc)}")
        print(f"Last Transaction Date: {fmt_date}")
        print(f"Title: {title}")
        print(f"Uniform Title: {uniform_title}")
        print(f"Author: {author}")
        print(f"Publisher: {publisher}")
        print(f"Publication Year: {pub_year}")
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
        print('-' * term_size.columns)

        exit(1)
        
