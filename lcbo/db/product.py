import traceback
from db.database import *
#from core.crawler import *

class Product:
    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        string = ''
        for k,v in vars(self).items():
            if k == 'img':
                string += k + '=' + str(v[:50]) + '...\n'
            else:
                string += k + '=' + str(v) + '\n'

        return string

    def save(self):
        try:
            # db = Database()
            db = Database(DBErrorHandler=DBExplodeOnError())

            # Create/Update the product record
            # db.query('insert into product (sku, name, img, description, price, size, alcohol, country, brewery) values (%s,%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update price=%s',
            db.query('select id from product where sku = %s limit 1', (self.sku))
            row = db.fetch_one()
            if row is None:
                print("row is none")
                db.query('insert into product (sku, name, description, price, size, alcohol, country, brewery,url,imgurl,"online_count") values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    (self.sku, self.name, self.description, self.price, self.size, self.alcohol, self.country, self.brewery,self.url,self.imgurl,self.online_count))
                db.query('select id from product where sku = %s limit 1', (self.sku))
                row = db.fetch_one()
                if row is None: return
            else:
                print("update row ",self.online_count,"row id ",row['id'])
                # db.query('update product (sku, name, img, description, price, size, alcohol, country, brewery,url,imgurl,online_count) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) where id = %s',
                #     (self.sku, self.name, b64decode(self.img), self.description, self.price, self.size, self.alcohol, self.country, self.brewery,self.url,self.imgurl,self.online_count, row['id']))
                db.query('update product set sku=%s, name=%s, description=%s, price=%s, size=%s, alcohol=%s, country=%s, brewery=%s, url=%s, imgurl=%s, online_count=%s where id = %s',
                    (self.sku, self.name, self.description, self.price, self.size, self.alcohol, self.country, self.brewery,self.url,self.imgurl,self.online_count, row['id']))

            # Write the time-series record
            db.query('insert into product_data (product_id, price) values (%s,%s)',
                (row['id'], self.price))
        except:
            print('should print traceback')
            print(traceback.print_exc())
    @classmethod
    def open(cls, id, sku):
        db = Database()
        # db = Database(DBErrorHandler=DBExplodeOnError())
        # Create/Update the product record
        # db.query('insert into product (sku, name, img, description, price, size, alcohol, country, brewery) values (%s,%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update price=%s',
        if id is None:
            db.query('select sku, name, img, description, price, size, alcohol, country, brewery,url,imgurl,online_count from product where sku = %s',sku)
        else:
            db.query('select sku, name, img, description, price, size, alcohol, country, brewery,url,imgurl,online_count from product where id = %s',id)

        row = db.fetch_one()
        p = Product()
        if not(row is None):
            sku = row['sku']
            name = row['name']
            img = row['img']
            description = row['description']
            price = row['price']
            size = row['size']
            alcohol = row['alcohol']
            country = row['country']
            brewery = row['brewery']
            url = row['url']
            imgurl = row['imgurl']
            online_count = row['online_count']
        else:
            name=''
            img=''
            description=''
            price=''
            size=''
            alcohol=''
            country=''
            brewery=''
            url=''
            imgurl=''
            online_count=''
        p.sku = sku
        p.name = name
        p.img = img
        p.description = description
        p.price = price
        p.size = size
        p.alcohol = alcohol
        p.country = country
        p.brewery = brewery
        p.url = url
        p.imgurl = imgurl
        p.online_count = online_count
        return p
