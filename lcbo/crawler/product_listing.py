#!/usr/bin/env python3

import re,traceback
from crawler.crawler import *
from db.product import *

class ProductListing(Crawler):
    def crawl(self):
        try:
            # Get product name
            prod_name = self.select_one('#prodName')

            # Image
            image = self.soup.select_one('.images img')['src']
            img_url = self.base_url + image
            print(img_url)
            image = Utils.fetch_source(img_url, stream=True)

            # retrieve and print just the sku number
            sku_reg_response = re.search(r'([0-9]+)', self.select_one('#prodSku'), re.I)
            if sku_reg_response:
                sku_reg_response = sku_reg_response.group()


            # Get product decription
            prod_description = self.select_one('.description blockquote')

            online_count = self.select_one('#'+sku_reg_response+'_onlineInventory')
            if online_count!= None:
                print('onlinecount '+ online_count)
            # FOO = self.select_one('#online-inventory')
            # FOO = self.select_one("online-inventory-out-of-stock")

            # TODO: FIX THIS
            # Get price value
            try:    prod_cur_price = self.select_one('.price .price-value')[1:]
            except: prod_cur_price = None

            # Attempt to find a saving price, if it exists, save it
            prod_saving = self.select('.price .saving')
            prod_saving = prod_saving[-1].get_text().strip() if prod_saving else None

            # Attempt to find a offer expiration date, if it exists, save it
            prod_LTO_end_date = self.select_one('.price .lto-end-date')
            LTO_reg_response = None
            if prod_LTO_end_date:
                LTO_reg_response = re.sub(r'(Limited Time Offer)', "", prod_LTO_end_date, re.I)

                if LTO_reg_response:
                    LTO_reg_response = LTO_reg_response.strip()

            # TODO: Make this suck less
            prod_details = self.soup.select_one('dl')
            s = [s.get_text().strip() for s in prod_details.contents if type(s) is not bs4.element.NavigableString]

            # Split string on spaces
            split_volume = s[0].split(' ')
            prod_container=''
            if len(split_volume)>2:
                # prod_size = size quantity + size metric
                prod_size = split_volume[0] + ' ' + split_volume[1]
                # prod_container = container type
                prod_container = split_volume[-1]
            elif len(split_volume)==2:
                # prod_size = size quantity + size metric
                prod_size = split_volume[0] + ' ' + split_volume[1]
            elif len(split_volume)==1:
                prod_size = s[0]
                prod_container = ''
            else:
                prod_size = ''
                prod_container = ''

            details_map = {}

            # Parse the details row, with the every other index being the key to the following value
            # Skipping the first two indexes as size does not follow this spec
            for i in range(2, len(s), 2):
                details_map[s[i]] = s[i+1]

            # TODO: Fix me some more
            alcohol_vol = details_map.get('Alcohol/Vol',None)
            if alcohol_vol is not None:
                alcohol_vol = alcohol_vol[:-1]

            # Create the object
            product = Product(
                category = None,
                name = prod_name,
                img = image,
                sku = sku_reg_response,
                description = prod_description,
                price = prod_cur_price,
                size = prod_size,
                container = prod_container,
                alcohol = alcohol_vol,
                country = details_map.get('Made in:',None),
                brewery = details_map.get('By:',None),
                style = details_map.get('Style:',None),
                url = self.url,
                imgurl = img_url,
                saving = prod_saving,
                expiration = LTO_reg_response,
                online_count = online_count
            )
            print(product)
            product.save()
        except:
            print(traceback.print_exc())
