import csv
import io
import zipfile
from datetime import datetime, timedelta
import enum
from itertools import count
from urllib import request

from bhavcopy import model


def fetch_bhav(date=None):
    if not date:
        date = datetime.today() - timedelta(1)

    url = 'https://www.bseindia.com/download/BhavCopy/Equity/EQ%s_CSV.ZIP' % date.strftime('%d%m%y')
    # Doesn't work midnight

    with request.urlopen(url) as response:
        z = zipfile.ZipFile(io.BytesIO(response.read()))

    csv_file_name = 'EQ%s.CSV' % date.strftime('%d%m%y')
    read_csv(csv_file_name, z)


def read_csv(fileName, z):

    csv_file = z.open(fileName)
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

        data.append(model.Equity(code, name, open, high, low, close))

    return data
