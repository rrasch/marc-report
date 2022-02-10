## About ##

Report of all MARC fields present in marcxml_in files

## Requirements ##

- python3
- pymarc

## Usage ##

To create a TSV file listing the number of tags encountered:

    ./count-tags.py -o <output_tsv> /path/to/marcxml_in/files

For example

    cd ~
    git clone https://github.com/rrasch/marc-report.git
    cd marc-report
    ./count-tags.py -o out.tsv /stuff/NNC/NNC_20180622/marcxml_in

To dump all records into a single csv file run:

    ./marc-report.py -o <output_csv> /path/to/marcxml_in/files

For example

    ./marc-report.py -o out.csv /stuff/NNC/NNC_20180622/marcxml_in

