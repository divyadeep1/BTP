import re
import scrapy
import os
from bs4 import BeautifulSoup
from analyzerBot.models import Review
from analyzerBot.utils import save_file



class reviews(scrapy.Spider):
    name="review1"


    review_list=[]
    start_urls= 'https://www.amazon.in/Nikon-D750-Digital-Lowepro-Hatchback/product-reviews/B01M062SQW/ref=cm_cr_arp_d_viewpnt_lft?showViewpoints=1&filterByStar=all_stars&pageNumber=1'
    product_name = re.split("/", start_urls)[3]
    def start_requests(self):
        yield scrapy.Request(self.start_urls,callback=self.parse,method='GET')
    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html.parser', from_encoding='utf-8')
        #print(soup.prettify())
        spans=soup.find_all('span',{'class':'a-size-base review-text review-text-content'})
        self.review_list.extend([span.get_text()for span in spans])
        next=soup.find('li',{'class':'a-last'})
        try:
            child=next.findChildren("a",recursive=False)[0]
            url=child.attrs['href']
            if url is not None:
                yield scrapy.Request(response.urljoin(url), callback=self.parse)
        except:
            self.clean()

    def remove_emoji_and_br(self, review_lists):
        rev = review_lists.replace("<br>", " ")
        rev = re.sub(
            r"[^A-Za-z0-9\.\!\?\s,\%\'\"\:\;\<\>\[\]\{\}\\\+\-\_\/]+", "", rev)
        rev = re.sub(r"\<a.+\<\/a\>", "url", rev)
        return rev

    def clean(self):
        clean_reviews = map(self.remove_emoji_and_br, self.review_list)
        with open('rev.txt', 'w') as f:
            for i, review in enumerate(clean_reviews):
                f.write(str(i)+". "+review+"\n\n")
            f.close();
        #return ReviewItem(product_name=self.product_name, file="rev.txt")
        review, created = Review.objects.get_or_create(product_name=self.product_name, file="rev.txt")
        save=save_file(review, "rev.txt")
        if save:
            os.remove("rev.txt")


