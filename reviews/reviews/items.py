
from scrapy_djangoitem import DjangoItem
from analyzerBot.models import Review


class ReviewItem(DjangoItem):
    django_model=Review
