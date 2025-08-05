# dnz_seochecker/crawler.py
import requests
from urllib.parse import urljoin, urlparse
from collections import deque
from dnz_seochecker.site_checker import SiteChecker
from dnz_seochecker.meta_checker import MetaChecker
from dnz_seochecker.link_checker import LinkChecker
from dnz_seochecker.seo_analyzer import SEOAnalyzer
from dnz_seochecker.ai_suggester import AISuggester

class Crawler:
    def __init__(self, start_url, max_pages=10, no_ai=False):
        self.start_url = start_url
        self.max_pages = max_pages
        self.no_ai = no_ai
        self.visited = set()
        self.to_visit = deque([start_url])
        self.reports = []

        parsed = urlparse(start_url)
        self.base_domain = parsed.netloc

    def is_internal(self, link):
        parsed_link = urlparse(link)
        return parsed_link.netloc == "" or parsed_link.netloc == self.base_domain

    def crawl(self):
        while self.to_visit and len(self.visited) < self.max_pages:
            url = self.to_visit.popleft()
            if url in self.visited:
                continue

            print(f"🔎 Crawling: {url}")
            try:
                site = SiteChecker(url)
                if not site.fetch():
                    continue

                self.visited.add(url)

                # Add new internal links
                for link in site.get_all_links():
                    full_link = urljoin(url, link)
                    if self.is_internal(full_link) and full_link not in self.visited:
                        self.to_visit.append(full_link)

                # Run your analysis logic
                meta_checker = MetaChecker(site.soup)
                link_checker = LinkChecker(url, site.get_all_links())
                broken_links = link_checker.check_links()

                report = {
                    "url": url,
                    "status_code": site.status_code,
                    "title": site.get_title(),
                    "meta": meta_checker.get_meta_tags(),
                    "description": meta_checker.get_description(),
                    "keywords": meta_checker.get_keywords(),
                    "broken_links": broken_links,
                    "images": site.get_images_with_alt()
                }

                analyzer = SEOAnalyzer(report, site.soup)
                suggestions = analyzer.run_all_checks()
                report["suggestions"] = suggestions

                if not self.no_ai:
                    try:
                        ai_suggester = AISuggester()
                        ai_text = ai_suggester.get_ai_suggestions(report)
                        report["ai_suggestions"] = ai_text
                    except Exception as e:
                        print(f"[WARNING] Could not get AI suggestions: {e}")

                self.reports.append(report)

            except Exception as e:
                print(f"[ERROR] Failed to crawl {url}: {e}")

        return self.reports
