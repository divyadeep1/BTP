import scrapy
import re


# Identified noise:
#   1.Emojis - replaced with ""
#   2.Line breaks <br> - replaced with " "
#   3.Hyperlinks - replaced with "url"
#   4.Links -


class reviewSpider(scrapy.Spider):
    name = "reviews"

    def __init__(self):
        self.reviews = []

    start_urls = [
        'https://www.amazon.in/Nikon-D750-Digital-Lowepro-Hatchback/product-reviews/B01M062SQW/ref=cm_cr_arp_d_viewpnt_lft?showViewpoints=1&filterByStar=positive&pageNumber=1'
    ]


    def remove_emoji_and_br(self, review):
        rev = review.replace("<br>", " ")
        rev = re.sub(
            r"[^A-Za-z0-9\.\!\?\s,\%\'\"\:\;\<\>\[\]\{\}\\\+\-\_\/]+", "", rev)
        rev = re.sub(r"\<a.+\<\/a\>", "url", rev)
        return rev

    def parse(self, response):

        self.reviews.extend(response.xpath("//span[@data-hook='review-body']").re(r'text">(.+)</span>'))
        print(len(self.reviews))

        next_page_url = response.css("li.a-last a::attr(href)").get()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse)
        else:
            self.clean()

    def clean(self):
        clean_reviews = map(self.remove_emoji_and_br, self.reviews)
        with open('rev.txt', 'w') as f:
            for i, review in enumerate(clean_reviews):
                f.write(str(i)+". "+review+"\n\n")
