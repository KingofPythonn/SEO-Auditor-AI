# dnz_seochecker/link_checker.py

import requests
from urllib.parse import urljoin

class LinkChecker:
    def __init__(self, base_url, links):
        self.base_url = base_url
        self.links = links
        self.broken_links = []

    def check_links(self, timeout=5):
        for link in self.links:
            absolute_url = urljoin(self.base_url, link)
            try:
                response = requests.head(absolute_url, timeout=timeout, allow_redirects=True)
                if response.status_code >= 400:
                    self.broken_links.append((absolute_url, response.status_code))
            except Exception as e:
                self.broken_links.append((absolute_url, str(e)))
        return self.broken_links
