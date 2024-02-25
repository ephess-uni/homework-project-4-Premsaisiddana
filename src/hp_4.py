# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    modified_date_list = []
    for dat in old_dates:
        modified_date_list.append(datetime.strptime(dat, "%Y-%m-%d").strftime("%d %b %Y"))
    return modified_date_list


def date_range(start, n):

    if not isinstance(start, str):
        raise TypeError
    elif not isinstance(n, int):
        raise TypeError
    else:
        added_list = []
        for inc in range(0, n):
            added_list.append(datetime.strptime(start, "%Y-%m-%d") + timedelta(days=inc))
        return added_list


def add_date_range(values, start_date):
    added_list = []
    for i, elem in enumerate(values):
        dat_list = []
        dat_list.append(datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i))
        dat_list.append(elem)
        added_list.append(tuple(dat_list))
    return added_list


def fees_report(infile, outfile):
    with open(infile) as file:
        added_list = []
        read_csv_obj = DictReader(file)
        for record in read_csv_obj:
            temp_dict = {}
            late_fee_days = datetime.strptime(record['date_returned'], '%m/%d/%Y') - datetime.strptime(
                record['date_due'], '%m/%d/%Y')
            if (late_fee_days.days > 0):
                temp_dict["patron_id"] = record['patron_id']
                temp_dict["late_fees"] = round(late_fee_days.days * 0.25, 2)
                added_list.append(temp_dict)
            else:
                temp_dict["patron_id"] = record['patron_id']
                temp_dict["late_fees"] = float(0)
                added_list.append(temp_dict)

        temp_dict_2 = {}
        for dict in added_list:
            key = (dict['patron_id'])
            temp_dict_2[key] = temp_dict_2.get(key, 0) + dict['late_fees']
        updated_list = [{'patron_id': key, 'late_fees': value} for key, value in temp_dict_2.items()]

        for dict in updated_list:
            for key, value in dict.items():
                if key == "late_fees":
                    if len(str(value).split('.')[-1]) != 2:
                        dict[key] = str(value) + "0"

    with open(outfile, "w", newline="") as file:
        col = ['patron_id', 'late_fees']
        writer = DictWriter(file, fieldnames=col)
        writer.writeheader()
        writer.writerows(updated_list)


if __name__ == '_main_':

    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    with open(OUTFILE) as f:
        print(f.read())