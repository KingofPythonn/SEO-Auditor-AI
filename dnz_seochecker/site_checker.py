# dnz_seochecker/site_checker.py

import requests
from bs4 import BeautifulSoup

class SiteChecker:
    def __init__(self, url, timeout=10):
        self.url = url
        self.timeout = timeout
        self.html = None
        self.soup = None
        self.status_code = None

    def fetch(self):
        try:
            response = requests.get(self.url, timeout=self.timeout)
            self.status_code = response.status_code
            if response.status_code == 200:
                self.html = response.text
                self.soup = BeautifulSoup(self.html, 'html.parser')
                return True
            else:
                return False
        except Exception as e:
            print(f"[ERROR] Could not fetch {self.url}: {e}")
            return False

    def get_title(self):
        if self.soup:
            title_tag = self.soup.find('title')
            return title_tag.text.strip() if title_tag else None
        return None

    def get_all_links(self):
        if self.soup:
            return [a.get('href') for a in self.soup.find_all('a', href=True)]
        return []

    def get_images_with_alt(self):
     if not self.soup:
        return []
     images = []
     for img in self.soup.find_all('img'):
        src = img.get('src')
        alt = img.get('alt')
        images.append({
            "src": src,
            "alt": alt
        })
     return images