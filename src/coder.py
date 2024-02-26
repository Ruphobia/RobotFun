import json
import requests

class CodeGenerator:
    def __init__(self):
        """Initialize the CodeGenerator with a fixed model and an empty context."""
        self.model = 'wizardcoder:33b'
        self.context = []  # Internal context to keep track of the conversation history
        self.callback = None
        print("Wizard Coder: Ready")

    def set_callback(self, callback_function):
        """
        Set the callback function to be used for handling the streamed output.
        
        :param callback_function: The function that handles streamed output.
        """
        self.callback = callback_function
        print("Wizard Coder Callback Ready")

    async def generate(self, prompt):
        """
        Generate code using the specified prompt and the internal context, streaming the output to the callback.
        
        :param prompt: The input prompt for code generation.
        """
        print("Generating:", prompt)

        r = requests.post('http://localhost:11434/api/generate',
                          json={
                              'model': self.model,
                              'prompt': prompt,
                              'context': self.context,
                              'keep_alive': -1,
                              'options': {'num_ctx': 4096},
                              
                          },
                          stream=True)
        r.raise_for_status()

        for line in r.iter_lines():
            body = json.loads(line)
            response_part = body.get('response', '')

            # Use the callback to handle the response part, if a callback is set
            if self.callback:
                print(response_part, end='', flush=True)
                await self.callback(response_part)
            else:
                # If no callback is set, default to printing the response part
                print(response_part, end='', flush=True)

            if 'error' in body:
                raise Exception(body['error'])

            if body.get('done', False):
                # Update the internal context with the new context returned by the model
                self.context = body['context']

    def clear_context(self):
        """Clear the internal context."""
        self.context = []