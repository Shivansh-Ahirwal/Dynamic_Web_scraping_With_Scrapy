from operator import itemgetter
import scrapy
from ..items import SunnyScrapingItem
import requests
from math import ceil

class sports_loisirs(scrapy.Spider):
    name = 'loisirs'
    start_urls =[
        'https://www.e.leclerc/api/rest/live-api/categories-tree-by-code/NAVIGATION_sport-loisirs?pageType=null&maxDepth=3'
    ]
    headers = {
        "accept": "application/json, text/plain, */*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    }

    def parse(self, response):
        items = SunnyScrapingItem()
        categories = self.extract_categories(response)
        for category in categories:
            
                for urll in category["url_list"]:  #category["url_list"] contains the all product's page urls in category

                    data = requests.get(urll,headers=self.headers)
                    raw_data= data.json()
                    
                    for item in raw_data["items"]:

                        items["collection"] = category["category"]

                        items["name"]=item["label"]
                        
                        for attr in item["attributeGroups"][0]["attributes"]:
                            if attr["code"]=="marque":
                                items["brand"]=attr["value"]["label"]

                        items["original_price"]=item["variants"][0]["offers"][0]["basePrice"]["totalPrice"]["price"]

                        #list product's image url
                        img_urls=[]
                        
                        for i in item["variants"][0]["attributes"]:
                            if i["type"]=="image":
                                items["image_url"] = i["value"]["url"]
            
                        items["product_page_url"]=str(urll)
                        
                        items["product_category"]=item["families"][1]["label"]
                        
                        #stock_status = True/False
                        if item["variants"][0]["offers"][0]["additionalFields"][1]["value"]=='in-stock':
                            items["stock"]=True
                        else:
                            items["stock"]=False

                        yield items
    

    def extract_categories(self,response):

        raw_data = response.json()
        categories=[]

        for data in raw_data["children"]:
            dct = {}
            dct["category"]=data["code"][11:].replace("-"," ")
            code=data["code"]
            num_of_products=data["nbProducts"]
            num_of_page=ceil(num_of_products/30)
            dct["number_of_page"] = num_of_page
            
            base_url="https://www.e.leclerc/api/rest/live-api/product-search?language=fr-FR&size=30&sorts=%5B%5D&page="
            
            suffix_url=code[11:]
            list_of_urls=[]

            for i in range(1,dct["number_of_page"]+1):
                url=base_url+str(i)+"&categories=%7B%22code%22:%5B%22"+code+"%22%5D%7D"
                list_of_urls.append(url)
            
            dct["url_list"]=list_of_urls

            categories.append(dct)

        return categories