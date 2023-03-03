import requests
from datetime import datetime
from bs4 import BeautifulSoup
from utils.config import Selectors
import re


class Data:
    def __init__(self, urls_data, golden_key):
        self.urls_data = urls_data
        self.golden_key = golden_key

    def worker(self):
        data = {}
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for url in self.urls_data:
            if self.golden_key:
                cks = {
                    'golden_key': self.golden_key
                }
            else:
                cks = None
            response = requests.get(url, cookies=cks)
            chip = re.findall('\/chips\/(\d+)\/', url)[0]
            soup = BeautifulSoup(response.text, 'lxml')
            title = soup.select_one('h1').text
            for server_number in self.urls_data[url]:
                server_code = soup.select(Selectors.servers)[
                    int(server_number)].attrs['value']
                items = soup.select(Selectors.item_s.format(server_code))[:10]
                for item in items:
                    amount = item.select_one(
                        Selectors.amount).text.strip().replace(' ', '')
                    try:
                        amount = int(amount)
                    except:
                        pass
                    try:
                        price = item.select_one(Selectors.price).text.strip()
                        price = float(price.split(' ')[0])
                    except:
                        pass
                    servername = item.select_one(
                        Selectors.servername).text.strip()
                    server = f'{server_code}-{chip}'
                    if not server in data:
                        data[server] = {
                            'title': title,
                            'servername': servername,
                            'amount': 0,
                            'price': 0,
                            'count': 0,
                            'prc': 0,
                            'time': timestamp
                        }
                    data[server]['amount'] += amount
                    data[server]['price'] += price * amount
                    data[server]['prc'] += price
                    data[server]['count'] += 1
        for server in data:
            data[server]['average'] = data[server]['prc'] / \
                data[server]['count']
        return data
