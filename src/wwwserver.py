#!/usr/bin/python3.8
# Python Includes
import os
import tornado.ioloop
from tornado.ioloop import IOLoop
import tornado.web
from sysmon import SysMonHandler, SysMon
import json
import asyncio

# application imports
from helpers import *
from intent import IntentClassifier
from coder import CodeGenerator
from question import QuestionGenerator

clients = []
promptclass = ""

class MainHandler(tornado.web.RequestHandler):
    def get(self, path=None):
        # Serve gpt.html as the default page instead of index.html
        if path is None or path == "":
            file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'www', 'gpt.html'))
        else:
            file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'www', path))
        
        # Check if the path exists and is a file (to prevent directory access)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                self.write(f.read())
            # Set the correct MIME type for .css and .js files
            if file_path.endswith(".css"):
                self.set_header("Content-Type", "text/css")
            elif file_path.endswith(".js"):
                self.set_header("Content-Type", "application/javascript")
        else:
            self.set_status(404)
            self.write("File not found")

class StreamHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        """Set headers for Server-Sent Events."""
        self.set_header('Content-Type', 'text/event-stream; charset=utf-8')
        self.set_header('Cache-Control', 'no-cache')
        self.set_header('Connection', 'keep-alive')

    async def get(self):
        clients.append(self)  # Add this connection to the list of clients
        print("Streaming Connected")
        # self.write(f"data: Connection established:{clients}\n\n")
        await self.flush()

        # Keep the connection open by waiting for a close event
        self.request.connection.stream.set_close_callback(self.on_connection_close)
        await self.wait_for_disconnect()
        print("Disconnected")

    def on_connection_close(self):
        # Remove the client from the list when the connection is closed
        clients.remove(self)
        print("Connection closed")

    async def wait_for_disconnect(self):
        """Wait indefinitely until the connection is closed."""
        while not self.request.connection.stream.closed():
            await tornado.gen.sleep(1)  # Sleep for a bit to prevent a busy-wait loop

    def check_origin(self, origin):
        # Override to allow connections from any origin
        return True

    def on_finish(self):
        # Ensure to clean up when the handler finishes
        if self in clients:
            clients.remove(self)

class PromptHandler(tornado.web.RequestHandler):
    # No need for SSE headers here since we're not streaming from this handler
    def post(self):
        global promptclass
        data = json.loads(self.request.body)
        prompt = data.get('prompt', '')
        print("Prompt:", prompt)
        save_Prompts(prompt)  # Assuming this is defined elsewhere
        promptclass = intentclassifier.classify_prompt(prompt)  # Assuming this is defined elsewhere
        print("Prompt Class:", promptclass)

        if (promptclass == "code"):
            IOLoop.current().spawn_callback(wizardcoder.generate, prompt)  

        if (promptclass == "question"):
            IOLoop.current().spawn_callback(wizardquestion.generate, prompt)  


class StopStreamHandler(tornado.web.RequestHandler):  
    def post(self):
        global promptclass
        print("Stop:", promptclass)
        if (promptclass == "code"):
            wizardcoder.request_stop()
        if (promptclass == "question"):
            wizardquestion.request_stop()

async def process_and_communicate_results(response):
    # print("Clients:", len(clients))
    for client in clients:
        try:
            # print("Writing data to client")
            formatted_response = f"data: {json.dumps(response)}\n\n"
            client.write(formatted_response)
            await client.flush()
            await asyncio.sleep(0)  # Allows the event loop to handle other tasks
        except Exception as e:
            print(f"Error sending data to client: {e}")

def make_app(sysmon_instance):
    return tornado.web.Application([
        (r"/api/sysmon", SysMonHandler, dict(sysmon_instance=sysmon_instance)),
        (r"/api/promptinput", PromptHandler),
        (r"/api/stream", StreamHandler),
        (r"/api/stopstream", StopStreamHandler),
        (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./www", "default_filename": "index.html"}),
    ])


intentclassifier = IntentClassifier()
systemmonitor = SysMon()
wizardcoder = CodeGenerator()
wizardcoder.set_callback(process_and_communicate_results)
wizardquestion = QuestionGenerator()
wizardquestion.set_callback(process_and_communicate_results)
print("Starting WWW Server")
app = make_app(systemmonitor)
app.listen(8888)
print("Server started at http://localhost:8888")
tornado.ioloop.IOLoop.current().start()
