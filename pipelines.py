import pymongo
from .items import SunnyScrapingItem

class MongoDBPipeline:

    collection = 'scrapy_items'

    def __init__(self):
        self.conn = pymongo.MongoClient('mongodb+srv://<username>:<password>@cluster0.qujskyo.mongodb.net/test')
        db = self.conn['scraped_data']
        self.collection = db['laclercdata']
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item
