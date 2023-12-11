import requests
import time
from bs4 import BeautifulSoup
from app.tools.proxy_finder import ProxyFinder


class FollowersParser(object):
    def __init__(self):
        self.proxy = ProxyFinder()
        self.appid = 552990
        self.followers_url = f'https://steamcommunity.com/games/{self.appid}/memberslistxml/?xml=1&l=english'+'&p={}'
        self.use_proxy_max = 5
        self.use_proxy = 0
        self.total_pages = 0
        self.total_followers = 0
        self.followers_list = []

    def get_total_pages_followers(self):
        res = requests.get(self.followers_url.format(1), proxies=self.proxy.active_proxy)
        soup = BeautifulSoup(res.text, 'xml')
        self.total_pages = int(soup.find('totalPages').text)
        res = requests.get(self.followers_url.format(self.total_pages), proxies=self.proxy.active_proxy)
        soup = BeautifulSoup(res.text, 'xml')
        self.total_followers = (self.total_pages - 1) * 1000 + len(soup.find_all('steamID64'))
        self.use_proxy += 2

    def get_steamids_from_page(self, page_number):
        # Repeate if data not received (by default)
        repeat = True
        while repeat is True:
            res = requests.get(self.followers_url.format(page_number), proxies=self.proxy.active_proxy)
            self.use_proxy += 1
            if res.status_code == 200 and self.use_proxy <= 5:
                soup = BeautifulSoup(res.text, 'xml')
                for steam_id_element in soup.find_all('steamID64'):
                    self.followers_list.append(int(steam_id_element.text))
                repeat = False
                
            else:
                self.proxy.change_proxy()
                self.use_proxy = 0

    def get_steamids_all_pages(self):
        start_time = time.time()
        self.followers_list = []
        if self.total_pages == 0:
            self.get_total_pages_followers()
        for page_number in range(1, self.total_pages+1):
            self.get_steamids_from_page(self, page_number)
        time_seconds = int((time.time() - start_time))
        return time_seconds