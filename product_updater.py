import mysql.connector

from Database.db_connector import DBConnector
from Page.product_list import ProductList
from selenium_session import SeleniumSession


class ProductUpdater:
    def __init__(self, config):
        self.config = config
        self.db = DBConnector(config).getDB()

    def update(self):
        seleniumSession = SeleniumSession(self.config)

        try:
            seleniumSession.initializeWebDriver()

            productList = ProductList(seleniumSession.getDriver(), self.config)
            productList.open()

            products = productList.getMyProducts()

            for product in products:
                product_exists = self.getProductByVintedId(product['id'])

                if not product_exists:
                    self.insertProduct(product)
                else:
                    if self.checkProductToUpdate(product, product_exists):
                        self.updateProduct(product, str(product_exists[0]))

        except Exception as e:
            print(f"An error occurred during the update process: {e}")

    def getProductByVintedId(self, id):
        try:
            sql = f"SELECT * FROM product WHERE id_vinted = {id}"

            cursor = self.db.cursor()
            cursor.execute(sql)

            return cursor.fetchone()
        except Exception as e:
            raise Exception(f"Error getting product by Vinted ID: {str(e)}")

    def checkProductToUpdate(self, product, product_exists):
        try:
            return str(product['updated_at']) != str(product_exists[len(product_exists) - 3])
        except Exception as e:
            raise Exception(f"Error checking if product needs to be updated: {str(e)}")

        return str(product['updated_at']) != str(product_exists[len(product_exists) - 3])

    def updateProduct(self, product, id):
        try:
            sql = "UPDATE product SET id_vinted = %s, title=%s, description=%s, brand=%s, label=%s, size=%s, status=%s, url=%s, price=%s, is_closed=%s, is_reserved=%s, is_hidden=%s, is_visible=%s, created_at=%s, updated_at=%s, to_sent=%s WHERE id_product=" + id

            val = (
                product['id'],
                product['title'],
                product['description'],
                product['brand'],
                product['label'],
                product['size'],
                product['status'],
                product['url'],
                product['price'],
                product['is_closed'],
                product['is_reserved'],
                product['is_hidden'],
                product['is_visible'],
                product['created_at'],
                product['updated_at'],
                0
            )

            cursor = self.db.cursor()
            cursor.execute(sql, val)

            self.deleteAllPhotosForProduct(id)
            self.insertPhotos(id, product['photos'])

            self.db.commit()
        except mysql.connector.Error as error:
            print("Database update failed: {}".format(error))
            self.db.rollback()

    def insertProduct(self, product):
        try:
            sql = "INSERT INTO product (id_vinted, title, description, brand, label, size, status, url, price, is_closed, is_reserved, is_hidden, is_visible, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            val = (
                product['id'],
                product['title'],
                product['description'],
                product['brand'],
                product['label'],
                product['size'],
                product['status'],
                product['url'],
                product['price'],
                product['is_closed'],
                product['is_reserved'],
                product['is_hidden'],
                product['is_visible'],
                product['created_at'],
                product['updated_at'],
            )

            cursor = self.db.cursor()
            cursor.execute(sql, val)

            last_product_id = int(cursor.lastrowid)

            self.insertPhotos(last_product_id, product['photos'])

            self.db.commit()
        except mysql.connector.Error as error:
            print("Database insert failed: {}".format(error))

            self.db.rollback()

    def insertPhotos(self, product_id, photos):
        try:
            cursor = self.db.cursor()

            sql = "INSERT INTO photo (id_product, id_vinted_photo, full_size_url, url, is_main, is_hidden) VALUES (%s, %s, %s, %s, %s, %s)"

            for photo in photos:
                val = (
                    product_id,
                    photo['id'],
                    photo['full_size_url'],
                    photo['url'],
                    photo['is_main'],
                    photo['is_hidden'],
                )

                cursor.execute(sql, val)
        except Exception as e:
            raise Exception(f"Error inserting photos: {str(e)}")

    def deleteAllPhotosForProduct(self, product_id):
        try:
            sql = "DELETE FROM photo WHERE id_product = " + product_id

            cursor = self.db.cursor()
            cursor.execute(sql)
        except Exception as e:
            raise Exception(f"Error deleting photos for product: {str(e)}")
