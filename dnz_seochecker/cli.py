
import typer
from dnz_seochecker.site_checker import SiteChecker
from dnz_seochecker.meta_checker import MetaChecker
from dnz_seochecker.link_checker import LinkChecker
from dnz_seochecker.report_generator import ReportGenerator
from dnz_seochecker.seo_analyzer import SEOAnalyzer
from dnz_seochecker.ai_suggester import AISuggester
from dnz_seochecker.crawler import Crawler


app = typer.Typer(help="A simple SEO analysis CLI tool in Python.")

@app.command()
def check(
    url: str = typer.Argument(..., help="The website URL to analyze."),
    output_json: str = typer.Option("report.json", help="Path for JSON report output."),
    output_html: str = typer.Option("report.html", help="Path for HTML report output."),
    no_ai: bool = typer.Option(False, help="Skip AI-powered analysis.")
):
    """
    Analyze the SEO of a single page and output JSON and/or HTML reports.
    """
    typer.echo(f"🔎 Checking site: {url}")

    site = SiteChecker(url)
    if not site.fetch():
        typer.echo("[ERROR] Failed to fetch the site.")
        raise typer.Exit(code=1)

    meta_checker = MetaChecker(site.soup)
    link_checker = LinkChecker(url, site.get_all_links())
    broken_links = link_checker.check_links()

    # Build report
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

    # Analyze with local rules
    analyzer = SEOAnalyzer(report, site.soup)
    suggestions = analyzer.run_all_checks()
    report["suggestions"] = suggestions

    # Optional AI Analysis
    if not no_ai:
        try:
            ai_suggester = AISuggester()
            ai_text = ai_suggester.get_ai_suggestions(report)
            report["ai_suggestions"] = ai_text

            typer.echo("\n✨ AI-Powered SEO Suggestions ✨")
            typer.echo(ai_text)
        except Exception as e:
            typer.echo(f"[WARNING] Could not get AI suggestions: {e}")

    # Write reports
    generator = ReportGenerator(report)
    generator.to_json(output_json)
    generator.to_html(output_html)

    typer.echo(f"\n✅ Reports generated:\n- {output_json}\n- {output_html}")



@app.command()
def crawl(
    url: str = typer.Argument(..., help="Root URL to crawl."),
    max_pages: int = typer.Option(10, help="Max number of pages to crawl."),
    output_json: str = typer.Option("site-report.json", help="Path for JSON report."),
    output_html: str = typer.Option("site-report.html", help="Path for HTML report."),
    no_ai: bool = typer.Option(False, help="Skip AI-powered analysis.")
  ):
    from dnz_seochecker.crawler import Crawler
    from dnz_seochecker.report_generator import ReportGenerator

    typer.echo(f"🌐 Starting crawl at {url} (max {max_pages} pages)")

    crawler = Crawler(url, max_pages=max_pages, no_ai=no_ai)
    reports = crawler.crawl()

    generator = ReportGenerator(reports)
    generator.to_json(output_json)
    generator.to_html(output_html)

    typer.echo(f"\n✅ Site crawl complete!")
    typer.echo(f"- JSON report: {output_json}")
    typer.echo(f"- HTML report: {output_html}")
   

# if __name__ == "__main__":
#     app()
