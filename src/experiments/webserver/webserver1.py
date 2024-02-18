#!/usr/bin/python3.8
import tornado.web
from tornado.httpserver import HTTPServer
import os
from jinja2 import Template

# Define our application
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # Get the current script's directory path using os.path.abspath(os.curdir)
        path = os.path.dirname(__file__) + "/"
        
        # Create an HTML template using Jinja2 that includes the story and CSS file
        html_template = Template("""
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>Robot Lost in the Woods</title>
                </head>
                <body style="font-family: Arial, sans-serif; color: #333;">
                    <header>
                        <h1 class="title">The Adventure of Robot R2D2</h1>
                    </header>
                    <main>
                        <section>
                            <p>Once upon a time, there was an intelligent robot named R2D2. 
It was on a routine mission in the woods when it suddenly got disoriented and lost its 
path.</p>
                            <p class="highlight">As darkness fell, R2D2 realized that it had 
to find its way back before the battery ran out.</p>
                        </section>
                        <section>
                            <h2>The Journey Begins</h2>
                            <p>R2D2 started its journey deeper into the woods, using its 
sensors to detect any signs of civilization or other robots. It communicated with its control
center through a weak signal, trying to get directions.</p>
                        </section>
                        <section>
                            <h2>Encountering Obstacles</h2>
                            <p class="highlight">Finally, a nearby rescue team detected 
R2D2's signal and started its rescue mission. They managed to reach it just in time before 
the battery ran out.</p>
                        </section>
                    </main>
                </body>
            </html>
        """)
        
        # Render the HTML template with CSS embedded into it
        css_file = open("styles.css", "r").read()
        complete_html = html_template.render(css=css_file)
        
        # Set the content type of the response to HTML
        self.set_header('Content-Type', 'text/html')
        
        # Write the rendered HTML to the HTTP response
        self.write(complete_html)

# Create an HTTP server that uses the previously defined application
if __name__ == "__main__":
    http_server = HTTPServer(MainHandler)
    try:
        print("Running on http://localhost:8000/")
        http_server.listen(8000)
        tornado.ioloop.IOLoop.current().start()  # Start Tornado's IOLoop, which is 
                                                 # responsible for handling asynchronous tasks
    except KeyboardInterrupt:
        pass

