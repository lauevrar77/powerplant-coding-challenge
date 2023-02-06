import falcon


class Healthcheck:
    def on_get(self, _, resp: falcon.Response):
        resp.media = {"success": True}
        resp.status = falcon.HTTP_200
