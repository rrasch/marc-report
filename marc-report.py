#!/usr/bin/env python3

from pprint import pprint
from pymarc import parse_xml_to_array

import argparse
import csv
import datetime
import glob
import logging
import pathlib
import os
import re
import struct

import constants
import leader

def parse_008_field(data):
    logging.debug(f"data={data}")
    logging.debug(f"template={constants.FF_TEMPLATE['BOOKS']}")

    start = 0

    bib_info = {}

    for i, field_len in enumerate(constants.FF_TEMPLATE['BOOKS']):
        len = int(field_len)
        logging.debug(len)
        end = start + len
        val = data[start:end].strip()

        logging.debug(f"{start}:{end-1}")

        name = constants.FF_FIELDS['BOOKS'][i]
        logging.debug(f"bib_info[{name}]: {val}")

        bib_info[name] = val
        if name == "Lang" and val in constants.LANG:
            bib_info["Language"] = constants.LANG[val]

        start = end

    return bib_info


def dump(obj):
    for attr in dir(obj):
        logging.debug("obj.%s = %r" % (attr, getattr(obj, attr)))

def format_date(tstamp):
    if re.search(r'^\d{14}\.0', tstamp):
        dt = datetime.datetime.strptime(tstamp, "%Y%m%d%H%M%S.%f")
        # return dt.strftime("%Y-%m-%d %H:%M")
        return dt.strftime("%c")
    else:
        return ""

def clean(buf):
    if buf:
        return buf.strip(" ,.:[]/")
    else:
        return ""

def get_field(record, tag):
    if tag in record:
        return clean(record[tag].format_field())
    else:
        return ""

def last_transaction_date(record):
    format_date(get_field(record, '005'))

def catalog_src(record):
    return get_field(record, '040')

def langcode(record):
    return get_field(record, '041')

def loc_call_number(record):
    return get_field(record, '050')

def lcl_call_number(record):
    return get_field(record, '099')

def publoc(record):
    return clean(record['260']['a'])

def myprint(desc, value):
    print('\033[92m' + desc + '\033[0m: ' + value)


columns = {
    "Record Length":          "record_length",
    "Record Status":          "record_status",
    "Record Type":            "record_type",
    "Bibliographic Level":    "bib_level",
    "Control Number":         "control_num",
    "Control Number ID":      "control_num_id",
    "Catalog Source":         "cat_src",
    "Language Code":          "lang_code",
    "LoC Call Number":        "loc_call_num",
    "Local Call Number":      "lcl_call_num",
    "Last Transaction Date":  "fmt_date",
    "System Control Number":  "syscn",
    "Title":                  "title",
    "Uniform Title":          "uniform_title",
    "Author":                 "author",
    "Publisher":              "publisher",
    "Publication Year":       "pub_year",
    "Publication Location":   "pub_loc",
    "ISBN":                   "isbn",
    "ISSN":                   "issn",
    "ISSN Title":             "issn_title",
    "ISSNL":                  "issnl",
    "Location":               "location",
    "Leader":                 "leader",
    "Notes":                  "notes",
    "Physical Description":   "phys_desc",
    "Subject":                "subjects",
    "Series":                 "series",
    "Superintendent of Doc":  "sudoc",
}



logging.basicConfig(
    format='%(asctime)s - marc-report - %(levelname)s - %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p')

parser = argparse.ArgumentParser(
    description="Report of all MARC fields present in marcxml_in files.")
parser.add_argument("input_dir", metavar="INPUT_DIRECTORY",
    help="Input directory")
parser.add_argument("-o", "--output", metavar="OUTPUT_FILE",
    required=True,
    help="Output csv file")
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

out = open(args.output, 'w', newline='')
writer = csv.writer(out, quotechar='"', quoting=csv.QUOTE_ALL)
writer.writerow(columns.keys())

for marc_file in marc_files:
    logging.debug(marc_file)

for marc_file in marc_files:
    logging.debug(marc_file)
    records = parse_xml_to_array(marc_file)
    for record in records:
        logging.debug(record)

        data = {}

        fields = record.get_fields()
        for field in fields:
            logging.debug(field)
            logging.debug(field.format_field())

        data['control_num'] = get_field(record, '001')
        data['control_num_id'] = get_field(record, '003')

        data['last_trans_date'] = get_field(record, '005')
        data['fmt_date'] = format_date(data['last_trans_date'])

        gen_info_str = record['008'].format_field()
        bib_info = parse_008_field(gen_info_str)

        data['lccn'] = get_field(record, '010')

        data['syscn'] = [entry.format_field()
            for entry in record.get_fields('035')]

        data['cat_src']       = catalog_src(record)      #040
        data['lang_code']     = langcode(record)         #041
        data['loc_call_num']  = get_field(record, '050') #050
        data['lcl_call_num']  = lcl_call_number(record)  #099

        ldr = leader.Leader(record.leader)
        logging.debug(ldr)

        data['leader']        = record.leader
        data['record_length'] = ldr.record_len
        data['record_status'] = ldr.record_status
        data['record_type']   = ldr.record_type
        data['bib_level']     = ldr.bib_level
        data['title']         = clean(record.title())
        data['uniform_title'] = clean(record.title())
        data['author']        = clean(record.author())
        data['publisher']     = clean(record.publisher())
        data['pub_year']      = clean(record.pubyear())
        data['pub_loc']       = clean(publoc(record))
        data['isbn']          = clean(record.isbn())
        data['issn']          = clean(record.issn())
        data['issn_title']    = clean(record.issn_title())
        data['issnl']         = clean(record.issnl())
        data['location']      = clean(record.location())
        data['sudoc']         = clean(record.sudoc())

        data['notes'] = [entry.format_field()
            for entry in record.notes()]

        data['phys_desc'] = [entry.format_field()
            for entry in record.physicaldescription()]

        data['subjects'] = [entry.format_field()
            for entry in record.subjects()]

        data['series'] = [entry.format_field()
            for entry in record.series()]

        print('-' * term_width)

        row = []

        for k, v in columns.items():
            val = ''
            if data[v]:
                if type(data[v]) is list:
                    val = ', '.join(data[v])
                else:
                    val = data[v]
                print(k + ': ', val)
            row.append(val)

        writer.writerow(row)

        fields = record.get_fields()
        for field in fields:
            print(f"[{field.tag}]", end="")
            if field.tag in constants.MARC_TAG:
                print(f" {constants.MARC_TAG[field.tag]}", end="")
            else:
                print(f"No description for {field.tag}")
                exit(1)
            print(f": {field.format_field()}")

        print(f"[008] Fixed Length Data Elements (Parsed):")
        for key, val in bib_info.items():
            if val and not re.search(r'^\|+$', val):
                print(f"\t{key}: '{val}'")

        print(f"[955] Locally Defined Field:")
        for entry in record.get_fields('955'):
            logging.debug(dir(entry))
            for key, value in entry.subfields_as_dict().items():
                logging.debug(f"{key} {value}")
                print(f"\t{constants.SUBFIELDS_955[key]}: {value[0]}")

