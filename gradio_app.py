import gradio as gr
from llm import Llama
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

client = QdrantClient(host="localhost", port=6333)
model = SentenceTransformer('all-MiniLM-L6-v2')

llama = Llama()
prompt_template_file = open("prompt_template.txt", "r")
prompt_template = prompt_template_file.read()

async def get_response(query):
    query_vector = model.encode(query)
    results = client.search(
        collection_name="rag_data",
        query_vector=query_vector,
        limit=10
    )
    context = ""
    for index, result in enumerate(results):
        context += f"Title : {result.payload['title']}\nLink : {result.payload['url']}\nContext {index} : {result.payload['description']}\n\n"
    response = ""
    async for word in llama.query(prompt_template.format(context, query)):
        response += word
        yield response

questions = [
    "Tell me how can I navigate to a specific pose - include replanning aspects in your answer., Can you provide me with code for this task?",
    "What are the primary goals of ROS 2 compared to ROS 1?",
    "How does Nav2 handle dynamic obstacles during navigation?",
    "How do you configure the Nav2 stack for a specific robot platform?",
    "What is the function of the costmap in Nav2, and how is it structured?"
]

with gr.Blocks() as demo:
    gr.Markdown("# Ros Question Answering System")
    
    inputs=gr.Dropdown(choices=questions, label="Choose a question")
    output_text = gr.Markdown(label="Streaming Output")
    
    submit_button = gr.Button("Generate Answer")
    
    submit_button.click(
        fn=get_response,
        inputs=inputs,
        outputs=output_text
    )

if __name__ == "__main__":
    demo.launch()