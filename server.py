import os
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"
from django.forms.models import model_to_dict
from models import Dog
import logging
import os.path
import tornado.escape
import tornado.httpclient
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=10000, help="Run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/([^/]+)", ClientHandler)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Welcome to Dogvibes!")


class ClientHandler(tornado.web.RequestHandler):
    def get(self, dogname):
        try:
            dog = Dog.objects.get(username=dogname)
        except Dog.DoesNotExist:
            self.write("No dog named <i>%s</i>. Wrong spelling?" % dogname)
            return
        self.render("index.html", dog=dog)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
