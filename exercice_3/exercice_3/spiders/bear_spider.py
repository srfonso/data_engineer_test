from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from exercice_3.settings import CONF_JSON_PATH
import json
import re

class WebSpider(CrawlSpider):
    name = "bearspace_spider"
    close_down = False

    start_urls = []
    allowed_domains = []

    # XPath of desired info
    title_xpath = ""
    desc_line1_xpath = ""
    desc_line2_xpath = ""
    price_xpath = ""

    # Regular expressions
    re_dims = "(\d+[\.\,]?\d*)\D*[xX×]\D*(\d+[\.\,]?\d*)"
    re_media = "(.+)"
    re_gbp = "£\s*(.*)"

    #Rules link to follow
    rules = (
        # Any URL with the below format will be parsed
        Rule(LinkExtractor(allow=r'https://www.bearspace.co.uk/product-page/.+'), callback='parse_item'),
    )


    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

        # Read configuration for this spider
        f = open(CONF_JSON_PATH,'r')
        config = json.load(f).get(self.name, {})
        if not config:
            raise Exception(f"Configuration for {self.name} doesn't exist.")

        self.allowed_domains = config["allowed_domains"]
        self.start_urls = config["start_urls"]
        self.title_xpath = config["title_xpath"]
        self.description_xpath = config["description_xpath"]
        self.price_xpath = config["price_xpath"]

        f.close()


    def parse_item(self, response):

        # NOTE: Sometimes media information appears in place of the dimensions and vice versa.
        desc_list = response.xpath(self.description_xpath).getall()
        try:
            height_cm, width_cm = self.extract_from_descr(desc_list, self.re_dims)
        except Exception as e:
            print(e)
            height_cm = None
            width_cm = None
            
        # first element once dimensions have been extracted is the media
        media = self.extract_from_descr(desc_list, self.re_media) 

        gbp = response.xpath(self.price_xpath).get()
        price_gbp = re.findall(self.re_gbp, gbp)[0]

        yield {
            "url": response.request.url,
            "title": response.xpath(self.title_xpath).get(),
            "media": media.replace("\n",""),
            "height_cm": height_cm,
            "width_cm": width_cm,
            "price_gbp": price_gbp
        }


    def extract_from_descr(self, list_str, regex):
        """ Extract the first one which match.
        Parameters
        ----------
        list_str: list
            List of strings
        regex: string
            Regular expression to use

        Returns
        -------
        ret: tuple | string
            First matched string
        """
        for str in list_str:
            re_list = re.findall(regex, str)
            if re_list:
                # Remove the matched element from list
                list_str.remove(str)
                return re_list[0]