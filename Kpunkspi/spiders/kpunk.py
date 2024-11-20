# The Story's Stroy blog scraper
# the goal of this project is to take all of the posts made to
# The Story's Story and turn them into a pd dataframe for spacy text annalysis

# find a way to ignore this part "Share this:ShareEmailFacebookRedditTwitterPrintLike this:Like Loading..."

import scrapy
from bs4 import BeautifulSoup
from items import kppost
from datetime import datetime
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.linkextractors import LinkExtractor


class KPunk(scrapy.Spider):
    name = "KPunk"
    allowed_domains = ["k-punk.org"]
    start_urls = ["http://k-punk.org/"]

    # parse will scape the archive section to collect a list of archive months
    def parse(self, response):
        extractor = LinkExtractor(
            # Got this via Inspect Element > Copy > XPath on the 'Archive' list element
            restrict_xpaths='/html/body/div/div[2]/div/div[2]/div[2]/div/div/ul[5]/li/ul'
        ).extract_links(response)

        for link in extractor:
            yield response.follow(link.url, callback=self.parse_month)


    # parse_month will scape the list of posts and collects their links
    def parse_month(self, response):
        # the 'Posts' list element
        extractor = LinkExtractor(
            restrict_xpaths='/html/body/div/div[2]/div/div[2]/div[1]/div'
        ).extract_links(response)
        
        for link in extractor:
            yield response.follow(link.url, callback=self.parse_post)

    # parse_post will read each post and scrapes it's content.
    def parse_post(self, response):
        yield None

    #     posts = response.xpath("//article")

    #     for post in posts:
    #         title_parts = post.css(".entry-title *::text").getall()
    #         title = " ".join([part.strip() for part in title_parts]).replace(
    #             "\xa0", " "
    #         )
    #         raw_html = post.css(".entry-content").get()
    #         soup = BeautifulSoup(raw_html, "html.parser")
    #         links = []
    #         text = soup.get_text()
    #         for p in soup.find_all("p"):
    #             for element in p.children:
    #                 if element.name == "a":
    #                     link_text = element.get_text()
    #                     link_url = element.get("href")
    #                     links.append({"url": link_url, "text": link_text})
    #                 else:
    #                     pass

    #         item = kppost(
    #             post_id=post.xpath("@id").get(),
    #             categories=post.css(".entry-categories a::text").getall(),
    #             tags=post.css(".entry-tags a::text").getall(),
    #             title=title,
    #             published_date=post.css(".entry-date a::text").get(),
    #             author=post.css(".author.vcard a::text").getall(),
    #             text=text,
    #             links=links,
    #         )
    #         yield item
