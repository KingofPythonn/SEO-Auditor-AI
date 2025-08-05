# dnz_seochecker/meta_checker.py

class MetaChecker:
    def __init__(self, soup):
        self.soup = soup

    def get_meta_tags(self):
        meta_data = {}
        for meta in self.soup.find_all('meta'):
            name = meta.get('name') or meta.get('property')
            content = meta.get('content')
            if name and content:
                meta_data[name.lower()] = content
        return meta_data

    def get_description(self):
        meta = self.soup.find('meta', attrs={'name': 'description'})
        if meta and meta.get('content'):
            return meta['content']
        return None

    def get_keywords(self):
        meta = self.soup.find('meta', attrs={'name': 'keywords'})
        if meta and meta.get('content'):
            return meta['content']
        return None
