import requests
from datetime import datetime
from bs4 import BeautifulSoup
from utils.config import Selectors


class Data:
    def __init__(self, urls_data):
        self.urls_data = urls_data

    def worker(self):
        data = {}
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for url in self.urls_data:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            for server_number in self.urls_data[url]:
                server_code = soup.select(Selectors.servers)[
                    int(server_number)].attrs['value']
                items = soup.select(Selectors.item_s.format(server_code))[:10]
                for item in items:
                    username = item.select_one(Selectors.username).text.strip()
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
                    server = server_code
                    if not server in data:
                        data[server] = {
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
