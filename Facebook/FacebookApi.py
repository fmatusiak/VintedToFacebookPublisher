import requests


class FacebookApi:
    def __init__(self, config):
        self.config = config

    def makePostRequest(self, url, data=None):
        try:
            resp = requests.post(url, data=data)

            resp.raise_for_status()

            return resp
        except Exception as e:
            raise Exception(f'Request failed. Error: {str(e)}')

    def addPost(self, message):
        requestUrl = f'https://graph.facebook.com/{self.config.get("facebook").get("id")}/feed?message={message}&access_token={self.config.get("facebook").get("token")}'

        return self.makePostRequest(requestUrl)

    def uploadUnpublishedPhoto(self, url):
        requestUrl = f'https://graph.facebook.com/{self.config.get("facebook").get("id")}/photos?url={url}&published=false&access_token={self.config.get("facebook").get("token")}'

        return self.makePostRequest(requestUrl)

    def updatePost(self, postId, message):
        requestUrl = f'https://graph.facebook.com/{postId}?message={message}&access_token={self.config.get("facebook").get("token")}'

        return self.makePostRequest(requestUrl)

    def addPostWithPhotos(self, message, photos):
        base_url = f'https://graph.facebook.com/{self.config.get("facebook").get("id")}/feed'

        mediaData = ','.join([f'{{"media_fbid": "{photo}"}}' for photo in photos])

        requestUrl = (
            f'{base_url}?'
            f'message={message}&'
            f'access_token={self.config.get("facebook").get("token")}&'
            f'attached_media=[{mediaData}]'
        )

        return self.makePostRequest(requestUrl)
