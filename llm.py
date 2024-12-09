import ollama

class Llama:

    def __init__(self, model="llama3.1:8b"):
        self.model = model

    async def query(self, prompt):
        message = {'role' : 'user', 'content': prompt}
        async for part in await ollama.AsyncClient().chat(model=self.model, messages=[message], stream=True):
            yield part['message']['content']

    def get_response(self, prompt):
        response = ollama.chat(
            model=self.model,
            messages=[
                {'role': 'user', 'content': prompt},
            ]
        )
        return response['message']['content']
