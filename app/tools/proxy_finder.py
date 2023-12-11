import requests
from bs4 import BeautifulSoup

class ProxyFinder(object):
    def __init__(self):
        self.proxies_list = self.get_proxies_list()
        self.active_proxy = self.get_working_proxy()

    def get_proxies_list(self):
        # Returns proxies in a list of dictionaries [{'159.223.183.111':'80'}]
        proxy_url = 'https://free-proxy-list.net/'
        res = requests.get(proxy_url)
        soup = BeautifulSoup(res.text, 'html.parser')
        proxies_list = []
        for tr in soup.find('tbody').find_all('tr'):
            proxies_list.append({tr.find_all('td')[0].text : tr.find_all('td')[1].text})
        return proxies_list

    def get_working_proxy(self):
        for proxy in self.proxies_list:
            status = requests.get('http://example.com', proxies=proxy).status_code
            if status == 200:
                return proxy
            else:
                self.proxies_list.remove(proxy)

    def change_proxy(self):
        if len(self.proxies_list) > 0:
            self.proxies_list.remove(self.active_proxy)
            self.active_proxy = self.get_working_proxy()
        else:
            self.proxies_list = self.get_proxies_list()


