import ollama

class Llama:

    def __init__(self, model="llama3.1:8b"):
        self.model = model

    async def query(self, prompt):
        message = {'role' : 'user', 'content': prompt}
        response = ""
        async for part in await ollama.AsyncClient().chat(model=self.model, messages=[message], stream=True):
            print(part['message']['content'], end='', flush=True)
            response += part['message']['content']
        print()
        return response

    def get_response(self, prompt):
        response = ollama.chat(
            model=self.model,
            messages=[
                {'role': 'user', 'content': prompt},
            ]
        )
        return response['message']['content']