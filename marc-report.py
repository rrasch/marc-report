#!/usr/bin/env python3

from pprint import pprint
from pymarc import parse_xml_to_array

import argparse
import csv
import glob
import logging

def dump(obj):
    for attr in dir(obj):
        print("obj.%s = %r" % (attr, getattr(obj, attr)))

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

logging.debug(marc_files)

for marc_file in marc_files:
    logging.debug(marc_file)
    records = parse_xml_to_array(marc_file)
    for record in records:
        logging.debug(record)
        print(dir(record))
        print("Title: {}".format(record.title()))
        print("Uniform Title: {}".format(record.uniformtitle()))
        print("Author: {}".format(record.author()))
        print("Publisher: {}".format(record.publisher()))
        print("Publication Year: {}".format(record.pubyear()))
        print("ISBN: {}".format(record.isbn()))
        print("ISSN: {}".format(record.issn()))
        print("ISSN Title: {}".format(record.issn_title()))
        record.leader()
#         print(foo)
#         print("Leader: {}".format(record.leader()))
#         print("Location: {}".format(record.location()))
#         print("Notes: {}".format(record.notes()))
#         print("Physical Description: {}".format(record.physicaldescription()))
# 
#         print("Series", record.subjects())
#         print("Subjects: {}".format(",".join(record.subjects()))

#         print("Superintendent of Documents (SuDoc): {}".format(record.sudoc()))


# , 'pos', 




        #dump(records)
#         fields = record.get_fields()
#         for field in fields:
#             print(vars(field))
#             print(field)

