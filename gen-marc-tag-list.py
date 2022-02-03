#!/usr/bin/env python3

import re
import pandas as pd
import tabula

pd.set_option("display.max_rows", None, "display.max_columns", None)

file = "marc21_codelist.pdf"

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

for index, row in df.iterrows():
    tag = row['MARC21']
    desc = row['Descriptions']
    if re.search(r'^\d{3}$', tag):
        if not re.search(r'\(.*\)', desc):
            desc = desc + " " + df.iloc[index + 1]['Descriptions']
        print(f"{tag},{desc}")

