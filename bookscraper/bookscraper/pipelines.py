# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter, adapter


class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # convert price to float and remove currency sign
        price_keys = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        for key in price_keys:
            price = adapter.get(key)
            adapter[key] = float(price.replace("£", ""))

        # convert star ratings to int
        text = adapter.get('stars')
        stars  = text.replace("star-rating ", "").strip()
        if stars == "One":
            adapter["stars"] = 1
        elif stars == "Two":
            adapter["stars"] = 2
        elif stars == "Three":
            adapter["stars"] = 3
        elif stars == "Four":
            adapter["stars"] = 4
        elif stars == "Five":
            adapter["stars"] = 5

        # change availability to to int
        text = adapter.get("availability")
        adapter["availability"] = text.split("(")[1].split()[0]

        return item
