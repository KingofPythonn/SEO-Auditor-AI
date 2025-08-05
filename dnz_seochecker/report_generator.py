

import json
import html

class ReportGenerator:
    def __init__(self, data):
        self.data = data

    def to_json(self, path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        print(f"[INFO] JSON report written to {path}")

    def to_html(self, path):
        html_content = self.build_html()
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"[INFO] HTML report written to {path}")

    def build_html(self):
        if isinstance(self.data, list):
            return self.build_multi_page_html()
        else:
            return self.build_single_page_html()

    def build_single_page_html(self):
        title = html.escape(self.data.get("title") or "No title found")
        url = html.escape(self.data.get("url") or "")
        status_code = self.data.get("status_code")

        meta = self.data.get("meta", {})
        broken_links = self.data.get("broken_links", [])
        suggestions = self.data.get("suggestions", [])
        ai_suggestions = self.data.get("ai_suggestions", "")

        def section(title, content):
            return f"<h2>{title}</h2>\n{content}"

        html_parts = [
            "<html><head><meta charset='utf-8'><title>SEO Report</title>",
            self._css(),
            "</head><body>",
            f"<h1>SEO Report for <a href='{url}'>{url}</a></h1>",
            f"<p><strong>Status Code:</strong> {status_code}</p>",
            f"<p><strong>Page Title:</strong> {title}</p>",
        ]

        # Meta Tags
        meta_html = "<ul>"
        for k, v in meta.items():
            meta_html += f"<li><strong>{html.escape(k)}:</strong> {html.escape(v)}</li>"
        meta_html += "</ul>"
        html_parts.append(section("Meta Tags", meta_html))

        # Images
        images = self.data.get("images", [])
        if images:
            images_html = "<ul>"
            for img in images:
                src = html.escape(img.get("src") or "")
                alt = img.get("alt")
                if alt and alt.strip():
                    images_html += f"<li class='ok'><strong>src:</strong> {src} | <strong>alt:</strong> {html.escape(alt)}</li>"
                else:
                    images_html += f"<li class='error'><strong>src:</strong> {src} | <strong>alt:</strong> MISSING</li>"
            images_html += "</ul>"
        else:
            images_html = "<p class='warn'>⚠️ No images found on this page.</p>"
        html_parts.append(section("Images and Alt Attributes", images_html))

        # Broken Links
        if broken_links:
            broken_html = "<ul>"
            for link, err in broken_links:
                err_text = html.escape(str(err))
                broken_html += f"<li class='error'>{html.escape(link)} → {err_text}</li>"
            broken_html += "</ul>"
        else:
            broken_html = "<p class='ok'>✅ No broken links found.</p>"
        html_parts.append(section("Broken Links", broken_html))

        # Suggestions
        sugg_html = "<ul>"
        for s in suggestions:
            s_class = "ok" if s.startswith("✅") else "warn" if s.startswith("⚠️") else "error"
            sugg_html += f"<li class='{s_class}'>{html.escape(s)}</li>"
        sugg_html += "</ul>"
        html_parts.append(section("Local Analysis Suggestions", sugg_html))

        # AI Suggestions
        if ai_suggestions:
            ai_html = f"<pre>{html.escape(ai_suggestions)}</pre>"
        else:
            ai_html = "<p class='warn'>⚠️ No AI suggestions generated.</p>"
        html_parts.append(section("AI-Powered SEO Suggestions", ai_html))

        html_parts.append("</body></html>")
        return "\n".join(html_parts)

    def build_multi_page_html(self):
        html_parts = [
            "<html><head><meta charset='utf-8'><title>SEO Site Crawl Report</title>",
            self._css(),
            "</head><body>",
            "<h1>SEO Site Crawl Report</h1>"
        ]

        for page in self.data:
            url = html.escape(page.get("url", ""))
            title = html.escape(page.get("title") or "No title found")
            status_code = page.get("status_code")

            meta = page.get("meta", {})
            broken_links = page.get("broken_links", [])
            suggestions = page.get("suggestions", [])
            ai_suggestions = page.get("ai_suggestions", "")
            images = page.get("images", [])

            html_parts.append("<hr>")
            html_parts.append(f"<h2>Page: <a href='{url}'>{url}</a></h2>")
            html_parts.append(f"<p><strong>Status Code:</strong> {status_code}</p>")
            html_parts.append(f"<p><strong>Page Title:</strong> {title}</p>")

            # Meta
            meta_html = "<ul>"
            for k, v in meta.items():
                meta_html += f"<li><strong>{html.escape(k)}:</strong> {html.escape(v)}</li>"
            meta_html += "</ul>"
            html_parts.append(f"<h3>Meta Tags</h3>\n{meta_html}")

            # Images
            if images:
                images_html = "<ul>"
                for img in images:
                    src = html.escape(img.get("src") or "")
                    alt = img.get("alt")
                    if alt and alt.strip():
                        images_html += f"<li class='ok'><strong>src:</strong> {src} | <strong>alt:</strong> {html.escape(alt)}</li>"
                    else:
                        images_html += f"<li class='error'><strong>src:</strong> {src} | <strong>alt:</strong> MISSING</li>"
                images_html += "</ul>"
            else:
                images_html = "<p class='warn'>⚠️ No images found on this page.</p>"
            html_parts.append(f"<h3>Images and Alt Attributes</h3>\n{images_html}")

            # Broken Links
            if broken_links:
                broken_html = "<ul>"
                for link, err in broken_links:
                    err_text = html.escape(str(err))
                    broken_html += f"<li class='error'>{html.escape(link)} → {err_text}</li>"
                broken_html += "</ul>"
            else:
                broken_html = "<p class='ok'>✅ No broken links found.</p>"
            html_parts.append(f"<h3>Broken Links</h3>\n{broken_html}")

            # Suggestions
            sugg_html = "<ul>"
            for s in suggestions:
                s_class = "ok" if s.startswith("✅") else "warn" if s.startswith("⚠️") else "error"
                sugg_html += f"<li class='{s_class}'>{html.escape(s)}</li>"
            sugg_html += "</ul>"
            html_parts.append(f"<h3>Local Analysis Suggestions</h3>\n{sugg_html}")

            # AI Suggestions
            if ai_suggestions:
                ai_html = f"<pre>{html.escape(ai_suggestions)}</pre>"
            else:
                ai_html = "<p class='warn'>⚠️ No AI suggestions generated.</p>"
            html_parts.append(f"<h3>AI-Powered SEO Suggestions</h3>\n{ai_html}")

        html_parts.append("</body></html>")
        return "\n".join(html_parts)

    def _css(self):
        return (
            "<style>"
            "body{font-family:sans-serif;line-height:1.6;padding:20px;}"
            "h1,h2,h3{color:#2c3e50;} "
            "ul{list-style:disc;margin-left:20px;} "
            ".error{color:red;} .ok{color:green;} .warn{color:orange;} "
            "pre{background:#f4f4f4;padding:10px;}"
            "</style>"
        )
