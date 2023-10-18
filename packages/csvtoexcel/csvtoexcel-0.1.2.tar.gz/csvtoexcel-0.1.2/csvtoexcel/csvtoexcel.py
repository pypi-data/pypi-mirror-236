import argparse
import csv
import re

from openpyxl import Workbook
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('csvfile', help='The .csv file to be converted')
parser.add_argument('-o,--output', dest='output', help='Name of the output file')
parser.add_argument(
    '-s,--auto-size',
    action='store_true',
    dest='auto_size',
    help='Resize columns to fit content',
)


def main():
    args = parser.parse_args()

    with open(args.csvfile) as input_file:

        # FROM: https://stackoverflow.com/a/68578582/118608
        match = ILLEGAL_CHARACTERS_RE.search(input_file.read())
        if match:
            input_file.seek(0)
            for lineno, line in enumerate(input_file.readlines()):
                line_match = ILLEGAL_CHARACTERS_RE.search(line)
                if line_match:
                    raise ValueError(
                        f'Illegal character in file on line {lineno + 1} at char {line_match.start()}'
                    )
        input_file.seek(0)

        reader = csv.reader(input_file)

        wb = Workbook()
        ws1 = wb.active
        ws1.title = 'Course'
        for row in reader:
            ws1.append(row)

    if args.auto_size:
        # Didn't auto size, but did make columns bigger
        # From: https://stackoverflow.com/a/68196124/118608
        # for idx, col in enumerate(ws1.columns, 1):
        #     ws1.column_dimensions[get_column_letter(idx)].auto_size = True

        # A combination of:
        # - https://stackoverflow.com/a/58150605/118608
        # - https://stackoverflow.com/a/39530676/118608
        for col in ws1.columns:
            column_letter = col[0].column_letter  # Get the column name
            max_length = max(len(str(cell.value)) for cell in col)
            # adjusted_width = (max_length + 2) * 1.2
            adjusted_width = max_length
            ws1.column_dimensions[column_letter].width = adjusted_width

    if args.output:
        output_filename = args.output
    else:
        output_filename = re.sub(r'\.csv$', '.xlsx', args.csvfile)
    with open(output_filename, 'wb') as output_file:
        wb.save(output_file)
