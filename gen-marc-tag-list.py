#!/usr/bin/env python3

import re
import pandas as pd
import tabula

pd.set_option("display.max_rows", None, "display.max_columns", None)

# wget https://www.inflibnet.ac.in/docs/marc21_codelist.pdf

file = "marc21_codelist.pdf"

# w3m -dump https://www.itsmarc.com/crs/mergedprojects/helpauth/helpauth/tag_list.htm > tag_list.txt
tag_list_file = "tag_list.txt"


pdopt = {
    'dtype': str,
}

tables = tabula.read_pdf(file, multiple_tables=False,
                               pages="all",
                               pandas_options=pdopt,
                               stream=True)

df = tables[0]

df.fillna('', inplace=True)

# print(df)

# print(df.columns)

tag_dict = {
    '019': 'OCLC Control Number Cross-Reference',
    '025': 'Overseas Acquisition Number (R)',
    '090': 'Locally Assigned LC-type Call Number (R)',
    '092': 'Locally Assigned Dewey Call Number (R)',
    '096': 'Locally Assigned NLM-type Call Number (R)',
    '098': 'Other Classification Schemes (R)',
    '099': 'Local Free-Text Call Number (R)',
    '337': 'Media Type (R)',
    '338': 'Carrier Type (R)',
    '360': 'Subject (R)',
    '648': 'Subject Added Entry-Chronological Term (R)',
    '655': 'Index Term-Genre/Form (R)',
    '776': 'Additional Physical Form Entry (R)',
    '797': 'Local Added Entry--Corporate Name (R)',
    '955': 'OCLC Locally Defined (R)',
}

for index, row in df.iterrows():
    tag = row['MARC21']
    desc = row['Descriptions']
    if re.search(r'^\d{3}$', tag):
        if not re.search(r'\(.*\)', desc):
            desc = desc + " " + df.iloc[index + 1]['Descriptions']
        tag_dict[tag] = desc

with open(tag_list_file) as f:
    lines = f.readlines()
    for line in lines:
        match = re.search(r'^(\d{3})\s+([^-].*)$', line)
        if match:
            tag = match.group(1)
            desc = match.group(2).strip()
            desc = re.sub(" +", " ", desc)
            if tag not in tag_dict and desc != "unassigned":
                tag_dict[tag] = desc

for tag, desc in sorted(tag_dict.items()):
    print(f"{tag},{desc}")

