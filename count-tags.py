#!/usr/bin/env python3

from pymarc import parse_xml_to_array
from collections import defaultdict

import argparse
import csv
import glob
import logging

logging.basicConfig(
    format='%(asctime)s - marc-report - %(levelname)s - %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p')

parser = argparse.ArgumentParser(
    description="Report of all MARC fields present in marcxml_in files.")
parser.add_argument("input_dir", metavar="INPUT_DIRECTORY",
    help="Input directory")
parser.add_argument("-o", "--output", metavar="OUTPUT_FILE",
    required=True,
    help="Output tsv file")
parser.add_argument("-d", "--debug",
    help="Enable debugging messages", action="store_true")
args = parser.parse_args()

if args.debug:
    logging.getLogger().setLevel(logging.DEBUG)

logging.debug("Input file: %s", args.input_dir)

marc_files = sorted(glob.glob(f"{args.input_dir}/*.xml"))

columns = ["Field",	"Subfield", "In Records", "Total"]

out = open(args.output, 'w', newline='')
writer = csv.writer(out, delimiter="\t")
writer.writerow(columns)

tag_count = defaultdict(dict)

sfield_count = defaultdict(dict)

for marc_file in marc_files:
    logging.debug(marc_file)
    records = parse_xml_to_array(marc_file)
    for record in records:
        logging.debug(record)
        seen = {}
        for field in record.get_fields():
            if field.tag not in seen:
                seen[field.tag] = True
                tag_count[field.tag]["uniq"] = (
                    tag_count[field.tag].get("uniq", 0) + 1)
            tag_count[field.tag]["all"] = (
                tag_count[field.tag].get("all", 0) + 1)
            
            if hasattr(field, 'subfields'):
                for code, value in field.subfields_as_dict().items():
                    logging.debug(f"{code} {value}")
                    sfield_count[field.tag][code] = (
                        sfield_count[field.tag].get(code, 0) + 1)

for tag in sorted(tag_count.keys()):
    writer.writerow([tag, "", tag_count[tag]["uniq"],
        tag_count[tag]["all"]])
    for code in sorted(sfield_count[tag].keys()):
        writer.writerow(["", f"${code}", "", sfield_count[tag][code]])

