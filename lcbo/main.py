#!/usr/bin/env python3
#----------------------------------------------------------------------------
# Author      : Carter Bourette
# Description : A simple python web scraper.
#               ...
#----------------------------------------------------------------------------
#

#from core.product_listing import *
from crawler.lcbo_crawler import *
from crawler.product_catalog import *
#from process_requests import *

if __name__ == "__main__":

    LCBOCrawler('http://www.lcbo.com/content/lcbo/en.html').crawl()
    # ProcessRequests().process()
    # ProductCatalog('foo').crawl()
    #ProductCatalog('http://www.lcbo.com/lcbo/catalog/dark/105002').crawl(0)
    #ProductCatalog('http://www.lcbo.com/lcbo/product/junction-craft-brewing-junction-road-black-lager/523720').crawl(0)
    #ProductCatalog('http://www.lcbo.com/lcbo/product/red-racer-across-the-nation-collaboration-west/603472').crawl(0)
