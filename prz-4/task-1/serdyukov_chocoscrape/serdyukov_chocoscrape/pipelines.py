# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import psycopg2

class SerdyukovChocoscrapePipeline:
    def process_item(self, item, spider):
        return item
    

class PriceConvertPipeline:
    exchange_rate = 1.3

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter.get('price'):
            adapter['price'] = round(float(adapter['price']) * self.exchange_rate, 2)
            return item
        else:
            raise DropItem(f"No price in {item}")
        
class RemoveDuplicatesPipeline:
    def __init__(self):
        self.names_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['name'] in self.names_seen:
            raise DropItem(f'duplicate found: {item!r}')
        else:
            self.names_seen.add(adapter['name'])
            return item
        
class PostgresPipeline(object):
    def __init__(self):
        self.create_connection()
    def create_connection(self):
        self.connection = psycopg2.connect(
            host="localhost",
            database="scrapydb",
            user="scrapy",
            password="P@ssw0rd!")
        self.curr = self.connection.cursor()
    def process_item(self, item, spider):
        self.store_db(item)
        return item
    def store_db(self, item):
        try:
            self.curr.execute(""" insert into chocolate_products (name, price, url) values (%s, %s, %s)""", (
                item["name"],
                item["price"],
                item["url"]
            ))

        except BaseException as e:
            print(e)
        self.connection.commit()