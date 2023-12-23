from datetime import datetime

from Database.DBConnector import DBConnector
from Facebook.FacebookApi import FacebookApi


class FacebookPublisher:
    def __init__(self, config):
        self.facebookApi = FacebookApi(config)
        self.db = DBConnector(config).getDB()

    def getProducts(self):
        try:
            sql = "SELECT * FROM product WHERE to_sent = 1 AND is_closed = 0 AND is_hidden = 0 AND is_visible = 1 ORDER BY created_at ASC"

            return self.executeQuery(sql)
        except Exception as e:
            raise Exception(f"Error getting products: {str(e)}")

    def getPhotosByProductId(self, productId):
        try:
            sql = f"SELECT * FROM photo WHERE is_hidden = 0 AND id_product = {productId}"

            return self.executeQuery(sql)
        except Exception as e:
            raise Exception(f"Error getting photos by product ID: {str(e)}")

    def executeQuery(self, sql):
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)

            return cursor.fetchall()
        except Exception as e:
            raise Exception(f"Error executing query: {str(e)}")

    def publish(self):
        try:
            self.publishPosts()
        except Exception as e:
            print(f'Error during publishing posts: {str(e)}')

    def publishPosts(self):
        products = self.mapDataToProducts(self.getProducts())

        for product in products:
            try:
                photos = self.mapDataToPhotos(self.getPhotosByProductId(product['id']))

                uploadPhotos = self.uploadPhotos(photos)

                message = self.generateMessage(product)
                postId = self.facebookApi.addPostWithPhotos(message, uploadPhotos).json()

                self.updateProduct(product['id'])

                print(f"Item with ID {product['id']} successfully posted on Facebook. Post ID: {postId}")
            except Exception as e:
                print(f'Error processing item with ID {product["id"]}. Error details: {str(e)}')

    def mapDataToProducts(self, data):
        return [
            {
                'id': product[0],
                'id_vinted': product[1],
                'title': product[2],
                'description': product[3],
                'brand': product[4],
                'label': product[5],
                'size': product[6],
                'status': product[7],
                'url': product[8],
                'price': product[9],
                'is_closed': product[10],
                'is_reserved': product[11],
                'is_hidden': product[12],
                'is_visible': product[13],
            } for product in data
        ]

    def mapDataToPhotos(self, data):
        return [
            {
                'id_photo': photo[0],
                'id_product': photo[1],
                'id_vinted_photo': photo[2],
                'full_size_url': photo[3],
                'url': photo[4],
                'is_main': photo[5],
                'is_hidden': photo[6],
            } for photo in data
        ]

    def updateProduct(self, productId):
        try:
            sql = f"UPDATE product SET to_sent = 0 WHERE id_product = {productId}"

            cursor = self.db.cursor()
            cursor.execute(sql)

            self.db.commit()
        except Exception as e:
            raise Exception(f"Error updating product: {str(e)}")

    def generateMessage(self, product):
        message = ''
        message += product['title'] + '\n\n'
        message += f"Rozmiar: {product['size']}\n"
        message += f"Stan: {product['status']}\n"
        message += f"Cena: {product['price']} zł\n\n"
        message += product['description'] + '\n\n'
        message += 'Zapraszam do zakupu\n' + product['url']

        return message

    def uploadPhotos(self, photos):
        try:
            return [
                self.facebookApi.uploadUnpublishedPhoto(photo['url']).json()['id'] for photo in photos
            ]

        except Exception as e:
            raise Exception(f"Error uploading photos: {str(e)}")

    def insertFbPhoto(self, photo, photoFbId):
        try:
            sql = "INSERT INTO facebook_photo (id_vinted_photo, id_product, fb_photo_id, upload_date) VALUES (%s, %s, %s, %s)"

            val = (
                photo['id_vinted_photo'],
                photo['id_product'],
                photoFbId,
                datetime.now().isoformat(),
            )

            cursor = self.db.cursor()
            cursor.execute(sql, val)

            self.db.commit()
        except Exception as e:
            raise Exception(f"Error inserting Facebook photo: {str(e)}")
