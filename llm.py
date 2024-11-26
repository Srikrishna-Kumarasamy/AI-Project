import asyncio
from ollama import AsyncClient

class Llama():

    def __init__(self):
        self.model = "llama3.1:8b"

    async def query(self, prompt):
        message = {'role' : 'user', 'content': prompt}
        async for part in await AsyncClient().chat(model=self.model, messages=[message], stream=True):
            print(part['message']['content'], end='', flush=True)
        print()
