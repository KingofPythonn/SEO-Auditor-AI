# dnz_seochecker/seo_analyzer.py

class SEOAnalyzer:
    def __init__(self, report, soup):
        self.report = report
        self.soup = soup
        self.suggestions = []

    def analyze_title(self):
        title = self.report.get('title')
        if not title:
            self.suggestions.append("❌ Missing <title> tag. Add a descriptive title.")
        elif len(title) < 10:
            self.suggestions.append(f"⚠️ Title is too short ({len(title)} chars). Make it more descriptive.")
        elif len(title) > 60:
            self.suggestions.append(f"⚠️ Title is long ({len(title)} chars). Consider shortening to ~60 chars.")
        else:
            self.suggestions.append("✅ Title length is good.")

    def analyze_description(self):
        desc = self.report.get('description')
        if not desc:
            self.suggestions.append("❌ Missing meta description. Add one around 150–160 chars.")
        elif len(desc) < 50:
            self.suggestions.append(f"⚠️ Description is short ({len(desc)} chars). Expand it.")
        elif len(desc) > 160:
            self.suggestions.append(f"⚠️ Description is long ({len(desc)} chars). Consider shortening.")
        else:
            self.suggestions.append("✅ Meta description length is good.")

    def analyze_keywords(self):
        keywords = self.report.get('keywords')
        if not keywords:
            self.suggestions.append("⚠️ No keywords meta tag. Not critical, but consider adding if helpful.")
        else:
            self.suggestions.append("✅ Keywords meta tag found.")

    def analyze_broken_links(self):
        broken = self.report.get('broken_links', [])
        if not broken:
            self.suggestions.append("✅ No broken links found.")
        elif len(broken) <= 5:
            self.suggestions.append(f"⚠️ {len(broken)} broken links found. Consider fixing them.")
        else:
            self.suggestions.append(f"❌ {len(broken)} broken links found. Major issue—fix them ASAP.")

    def analyze_viewport(self):
        viewport = self.report['meta'].get('viewport')
        if not viewport:
            self.suggestions.append("⚠️ Missing viewport meta tag. Add for mobile responsiveness.")
        else:
            self.suggestions.append("✅ Viewport meta tag found.")

    def analyze_h1(self):
        h1_tags = self.soup.find_all('h1')
        if not h1_tags:
            self.suggestions.append("❌ No <h1> tag found. Add a main heading.")
        elif len(h1_tags) > 1:
            self.suggestions.append(f"⚠️ Multiple <h1> tags found ({len(h1_tags)}). Ideally use one.")
        else:
            self.suggestions.append("✅ Single <h1> tag found.")

    
    def analyze_image_alt(self):
     images = self.report.get('images', [])
     missing_alt = [img for img in images if not img.get('alt') or img.get('alt').strip() == ""]

     if not images:
         self.suggestions.append("⚠️ No <img> tags found on the page.")
     elif not missing_alt:
        self.suggestions.append("✅ All images have alt text.")
     else:
        self.suggestions.append(f"❌ {len(missing_alt)} images missing alt text. Add descriptive alt attributes for accessibility and SEO.")

    
    def run_all_checks(self):
        self.analyze_title()
        self.analyze_description()
        self.analyze_keywords()
        self.analyze_broken_links()
        self.analyze_viewport()
        self.analyze_h1()
        self.analyze_image_alt()

        return self.suggestions
    