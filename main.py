import time
from utils import google_sheets
from data.scraper import Data


def read_urls_file():
    urls_data = {}
    with open('urls.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            url, servers = line.split(',', maxsplit=1)
            urls_data[url.strip()] = [s.strip() for s in servers.split(',')]
    return urls_data


def scraper():
    urls_data = read_urls_file()
    data = Data(urls_data).worker()
    return data


def uploader(data):
    sheet = google_sheets.upload_data([
        [
            data[d]['servername'],
            data[d]['amount'],
            data[d]['price'],
            data[d]['average'],
            data[d]['time'],
        ] for d in data
    ], 'stocks-data')
    print('DATA UPLOADED AT: {}'.format(sheet))


def worker():
    data = scraper()
    uploader(data)


while True:
    worker()
    time.sleep(1800)
