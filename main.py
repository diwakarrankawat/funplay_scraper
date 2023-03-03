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


def check_golden_key():
    try:
        with open('key.txt') as fl:
            golden_key = fl.read().strip()
    except:
        golden_key = None
    return golden_key


def scraper():
    urls_data = read_urls_file()
    golden_key = check_golden_key()
    data = Data(urls_data, golden_key).worker()
    return data


def uploader(data):
    sheet = google_sheets.upload_data([
        [
            data[d]['title'],
            data[d]['servername'],
            data[d]['amount'],
            data[d]['price'],
            data[d]['average'],
            data[d]['time'],
        ] for d in data
        # ], 'stocks-data')
    ], 'test')
    print('DATA UPLOADED AT: {}'.format(sheet))


def worker():
    data = scraper()
    uploader(data)


while True:
    worker()
    time.sleep(1800)
