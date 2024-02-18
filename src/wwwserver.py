#!/usr/bin/python3.8
# Python Includes
import os
import tornado.ioloop
import tornado.web
from sysmon import SysMonHandler, SysMon

class MainHandler(tornado.web.RequestHandler):
    def get(self, path=None):
        if path is None or path == "":
            file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'www', 'index.html'))
        else:
            file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'www', path))
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                self.write(f.read())
        else:
            self.set_status(404)
            self.write("File not found")

def make_app(sysmon_instance):
    return tornado.web.Application([
        (r"/api/sysmon", SysMonHandler, dict(sysmon_instance=sysmon_instance)),
        (r"/(.*)", MainHandler),
    ])

if __name__ == "__main__":
    systemmonitor = SysMon()
    app = make_app(systemmonitor)
    app.listen(8888)
    print("Server started at http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()
