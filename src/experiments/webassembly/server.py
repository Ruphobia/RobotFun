#!/usr/bin/python3.8

# compile web assembly program:
# wat2wasm move_dot.wat -o move_dot.wasm

import os
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    """Serve the index.html file as the main page."""
    def get(self):
        self.render("index.html")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/(.*)", tornado.web.StaticFileHandler, {"path": os.getcwd()}),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    print("Server is running at http://localhost:8080")
    tornado.ioloop.IOLoop.current().start()
