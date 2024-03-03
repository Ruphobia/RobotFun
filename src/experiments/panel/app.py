#!/usr/bin/python3
import panel as pn
from bokeh.server.server import Server

pn.extension()

# Function to create the application layout
def create_app(doc):
    header = pn.pane.Markdown("# Simple Chatbot Interface", styles={'background': '#d1ecf1'}, sizing_mode='stretch_width')
    chat_area = pn.Column(sizing_mode='stretch_both', max_height=400, scroll=True, styles={'background': '#f0f0f0'})
    input_box = pn.widgets.TextInput(name='Your message:', sizing_mode='stretch_width')
    send_button = pn.widgets.Button(name='Send', button_type='primary')
    stop_button = pn.widgets.Button(name='Stop', button_type='danger')

    # Define the stop chat function correctly before using it
    def stop_chat(event):
        input_box.disabled = True  # Disable the input box
        send_button.disabled = True  # Disable the send button
        stop_button.disabled = True  # Optionally disable the stop button itself to prevent further clicks

    # Define the chatbot function
    def simple_chatbot(event):
        input_text = input_box.value
        add_message_to_chat(f'You: {input_text}')  # Add the user's message to the chat
        input_box.value = ''  # Clear the input box after sending

    send_button.on_click(simple_chatbot)
    stop_button.on_click(stop_chat)

    # Function to add a message to the chat area
    def add_message_to_chat(message, is_code=False):
        if is_code:
            # Header for the code window
            code_header = pn.pane.Markdown("### Python", margin=(0,10))

            # Button to copy code to clipboard
            copy_button = pn.widgets.Button(name='Copy to Clipboard', button_type='success', width=150, align='end')
            # Setting the JavaScript code directly for the button's on-click event
            copy_button.js_on_click(code="""
                navigator.clipboard.writeText(code);
                """, args={'code': message})

            # Composite widget for the code window
            code_window = pn.Column(code_header, pn.pane.Markdown(message, background='#e8e8e8', margin=(5,10)), copy_button, margin=(10,10))
            chat_area.append(code_window)
        else:
            # Add a regular message as a Markdown pane
            chat_area.append(pn.pane.Markdown(f"- {message}", margin=(5,10)))

    # Example Python code snippet using Markdown for syntax highlighting
    code_snippet = """```python
# Example Python function
def hello_world():
    print("Hello, world!")
```"""
    add_message_to_chat(code_snippet, is_code=True)

    # Bottom prompt layout includes the input box and buttons
    prompt_area = pn.Row(input_box, send_button, stop_button, sizing_mode='stretch_width')

    # Main layout
    main_layout = pn.Column(header, chat_area, prompt_area, sizing_mode='stretch_width')

    doc.add_root(main_layout.get_root(doc))

# Start the Bokeh server with the specified port
server = Server({'/': create_app}, port=5006)
server.start()

# Optionally open a browser window to the application
server.io_loop.add_callback(server.show, "/")

# Start the server's I/O loop
server.io_loop.start()
