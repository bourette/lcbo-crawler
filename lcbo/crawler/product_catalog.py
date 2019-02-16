#!/usr/bin/env python3

#from core.crawler import *
from crawler.product_listing import *
from db.request import *
from db.product import *

class ProductCatalog(Crawler):

    def get_query_params(self, page_num):
        return {
          'contentBeginIndex': '0',
          'productBeginIndex': str((page_num - 1) * 12),
          'beginIndex': str((page_num - 1) * 12),
          'orderBy': '',
          'pageView': '',
          'resultType': 'products',
          'orderByContent': '',
          'searchTerm': '',
          'facet': '',
          'storeId': '10151',
          'catalogId': '10001',
          'langId': '-1',
          'fromPage': '',
          'loginError': '',
          'userId': '-1002',
          'objectId': '',
          'requesttype': 'ajax'
        }

    def crawl(self, keepgoing=1):
        page_counter = 1

        while True:
            products = self.select('.product')

            # When there are no more products, quit
            if len(products) < 1: break
            # TODO: Fix? We need to break if we're stuck in loop
            if page_counter > 300: break

            # Collect the individual links from catalog and create listing crawler
            for p in products:
                ok = self.saveItem(p)
            # When we are done the current page, request the next, rinse repeat
            page_counter += 1
            if keepgoing == 1:
                self.load_page(self.url, withAjax=True, payload=self.get_query_params(page_counter))
            else:
                return

    def saveItem(self, p):
        try:
            link = p.div.div.a['href']
            print('Create listing for ' + link)
            sku = p['data-product-sku']
            product = Product.open(None,sku)
            product.name = p.div.div.a.get_text()
            sizetext = p.div.div.small.span.get_text()
            # print('sizetext',sizetext)
            product.size = sizetext.split('| ')[1]
            product.price = p.select_one('.price').get_text().strip('$')
            # print('price is',price)
            # pp = '#product_price_'+sku
            # for div in p:
            #     print('lookat div',div)
            #     if 'product_price_' in div:
            #         print('pricediv',div)
            # print("pp",pp)
            # pricediv = self.select_one(pp)
            # print("pricediv",pricediv)
            # print(p.div.div)
            # seldiv = p.div.div.find_next_siblings()
            # print(p.div)
            # print('sku' + sku)
            #print(nextdiv[1])
            # online_count = p.div.select('#'+sku+'_onlineInventory')
            #online_count = p.div.select('.online .in-stock')
            #print("online_count ",online_count)
            # id="190439_onlineInventory"
            # if online_count != None:
            #     online_count = online_count.get_text()
            #     print('online_count',online_count)
            # product.online_count = online_count
            # print('p.div',p.select_one('#product_price_'))
            # print(seldiv)
            # print(nextdiv[1].div.div.get_text())
            #print("price",p.div.div[2].div.div.get_text())
            # print('size',size)
            product.url = link
            # product.size = size
            # self.url,self.imgurl

            # sizes = p.div.div.small.findAll('span')
            # for span in sizes:
            #     print('top',span)
            #     if "class" in span:
            #         print('in spans ',span["class"])
            #         if (span["class"]=="plp-volume"):
            #             print ('full',span)
            # print('v0',p.select_one("span.plp-volume plp-volume-list"))
            # print("vl", p.select_one('#plp-volume plp-volume-list'))
            # print('vl2',self.select_one('#plp-volume plp-volume-list'))
            # size = self.select_one("#plp-volume plp-volume-list")
            request = Request(
                baseurl = self.base_url,
                endpoint = link
            )
            print(request)
            request.save()
            product.save()
            return 1
            # sku_reg_response = re.search(r'([0-9]+)', p.select_one('#prodSku'), re.I)
            # if sku_reg_response:
            #     sku_reg_response = sku_reg_response.group()
            #     online_count = self.select_one('#'+sku_reg_response+'_onlineInventory')
            #     print('online count ',online_count)
            # #ProductListing(self.base_url + link).crawl()
            # # Create the object
            # product.online_count = online_count
        except:
            print(traceback.print_exc())
            return 0
