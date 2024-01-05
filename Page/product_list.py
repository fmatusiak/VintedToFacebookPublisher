import dateutil.parser as dt
import pytz


class ProductList:
    def __init__(self, driver, config):
        self.driver = driver

        self.__base_url = config.get('vinted').get('base_url_profile')
        self.__member = config.get('vinted').get('member')

    def open(self):
        try:
            self.driver.get(f"{self.__base_url}{self.__member}")
        except Exception as e:
            print(f"Error during page opening: {e}")

    def fetchMyProducts(self, page):
        url = f"https://www.vinted.pl/api/v2/users/{self.__member}/items?page={page}&per_page=20&order=relevance&currency=PLN"
        return self.fetchXhr(url)

    def fetchXhr(self, url):
        try:
            js = """((cb) => {
                   fetch('%s').then(resp => resp.json()).then(cb)
               })(...arguments)
               """ % url

            return self.driver.execute_async_script(js)
        except Exception as e:
            print(f"Error during XHR fetch: {e}")

    def getMyProducts(self):
        try:
            products_list = self.fetchMyProducts(1)
            products = list(products_list['items'])

            total_pages = products_list['pagination']['total_pages']
            current_page = products_list['pagination']['current_page'] + 1

            while current_page <= total_pages:
                products_list = self.fetchMyProducts(current_page)

                for item in products_list['items']:
                    products.append(item)

                current_page = products_list['pagination']['current_page'] + 1

            product_parser = ProductParser()
            parsed_products = [product_parser.parse(item) for item in products]

            print("Count my products: " + str(len(parsed_products)))

            return parsed_products
        except Exception as e:
            print(f"Error during fetching products: {e}")


class ProductParser:
    def parse(self, product):
        try:
            data = {
                'id': product['id'],
                'title': product['title'],
                'description': product['description'],
                'brand': product['brand'],
                'label': product['label'],
                'size': product['size'],
                'status': product['status'],
                'url': product['url'],
                'price': product['price_numeric'],
                'is_closed': product['is_closed'],
                'is_reserved': product['is_reserved'],
                'is_hidden': product['is_hidden'],
                'is_visible': product['is_visible'],
                'created_at': self.parseDate(product['created_at_ts']),
                'updated_at': self.parseDate(product['updated_at_ts'])
            }

            photos = [{
                'id': photo['id'],
                'full_size_url': photo['full_size_url'],
                'url': photo['url'],
                'is_main': photo['is_main'],
                'is_hidden': photo['is_hidden'],
            } for photo in product['photos']]

            data['photos'] = photos

            return data
        except Exception as e:
            print(f"Error during product parsing: {e}")

    def parseDate(self, string):
        try:
            parse_date = dt.parse(string)

            return pytz.timezone("UTC").normalize(parse_date).strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            print(f"Error during date parsing: {e}")
