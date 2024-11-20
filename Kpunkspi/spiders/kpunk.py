# The Story's Stroy blog scraper
# the goal of this project is to take all of the posts made to
# The Story's Story and turn them into a pd dataframe for spacy text annalysis

# find a way to ignore this part "Share this:ShareEmailFacebookRedditTwitterPrintLike this:Like Loading..."

import scrapy
from scrapy.http import Response
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
    def parse(self, response: Response):
        extractor = LinkExtractor(
            # Got this via Inspect Element > Copy > XPath on the 'Archive' list element
            restrict_xpaths='/html/body/div/div[2]/div/div[2]/div[2]/div/div/ul[5]/li/ul'
        ).extract_links(response)

        for link in extractor:
            yield response.follow(link.url, callback=self.parse_month)


    # parse_month will scape the list of posts and collects their links
    def parse_month(self, response: Response):
        # the 'Posts' list element
        extractor = LinkExtractor(
            restrict_xpaths='/html/body/div/div[2]/div/div[2]/div[1]/div'
        ).extract_links(response)
        
        for link in extractor:
            yield response.follow(link.url, callback=self.parse_post)

    # parse_post will read each post and scrapes it's content.
    def parse_post(self, response: Response):
        # Start of post
        post = response.selector.xpath("/html/body/div[1]/div[2]/div/div[1]")

        title = post.xpath("/html/body/div[1]/div[2]/div/div[1]/h2/a/text()").get()
        
        date = post.xpath("/html/body/div/div[2]/div/div[1]/small[1]/text()").get()

        post_id = post.xpath("/html/body/div/div[2]/div/div[1]/h2/@id").get() \
            .split('-')[1]  # 'post-1309' -> 1309
        

        post_categories = post.xpath("/html/body/div/div[2]/div/div[1]/small[2]").css('a::text').getall()

        
        # Parse HTML and extract Text content
        raw_html = post.css(".entrytext").get()
        soup = BeautifulSoup(raw_html, "html.parser")
        post_text = soup.get_text()

        item = kppost(
            # post_id=post.xpath("@id").get(),
            categories=post_categories,
            # tags=post.css(".entry-tags a::text").getall(),
            title=title,
            published_date=date,
            # author=post.css(".author.vcard a::text").getall(),
            text=post_text,
        )
        yield item
