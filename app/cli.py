
import csv

from app.tools.proxy_finder import ProxyFinder
from app.tools.followers_parser import FollowersParser

followers_parser = FollowersParser()


followers_parser.get_total_pages_followers()

followers_parser.followers_list
followers_parser.total_pages

for page_number in range(250, 502):
    print(followers_parser.proxy.active_proxy)
    followers_parser.get_steamids_from_page(page_number)
    print(page_number)



with open('followers2.csv', 'w') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerows(followers_parser.followers_list)
