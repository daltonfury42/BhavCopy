import csv
import io
import zipfile
from datetime import datetime, timedelta
import enum
from itertools import count
from urllib import request, error

from bhavcopy import model


class BhavNotFoundException(BaseException):
    pass


def fetch_bhav(date):
    url = 'https://www.bseindia.com/download/BhavCopy/Equity/EQ%s_CSV.ZIP' % date.strftime('%d%m%y')
    # Doesn't work midnight
    #hi

    try:
        with request.urlopen(url) as response:
            z = zipfile.ZipFile(io.BytesIO(response.read()))
    except error.HTTPError as e:
        raise BhavNotFoundException

    return read_csv(z, date)


def read_csv(z, date):

    file_name = 'EQ%s.CSV' % date.strftime('%d%m%y')

    csv_file = z.open(file_name)
    csv_file = io.TextIOWrapper(csv_file)
    csv_reader = csv.reader(csv_file, delimiter=',')

    header_row = next(csv_reader)
    header = enum.Enum('CsvHeader', zip(header_row, count()))

    data = []
    for row in csv_reader:
        code = int(row[header.SC_CODE.value])
        name = row[header.SC_NAME.value].strip()
        open = float(row[header.OPEN.value])
        high = float(row[header.HIGH.value])
        low = float(row[header.LOW.value])
        close = float(row[header.CLOSE.value])

        data.append(model.Equity(code=code,
                                 name=name,
                                 open=open,
                                 high=high,
                                 low=low,
                                 close=close,
                                 date=date))

    return data
