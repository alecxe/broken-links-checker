from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.item import Item, Field


class GitHubLinkItem(Item):
    url = Field()
    referer = Field()
    status = Field()


class GithubHelpSpider(CrawlSpider):
    name = "github_help"
    allowed_domains = ["help.github.com"]
    start_urls = ["https://help.github.com", ]
    handle_httpstatus_list = [404]
    rules = (Rule(SgmlLinkExtractor(), callback='parse_item', follow=True),)

    def parse_item(self, response):
        if response.status == 404:
            item = GitHubLinkItem()
            item['url'] = response.url
            item['referer'] = response.request.headers.get('Referer')
            item['status'] = response.status

            return item
