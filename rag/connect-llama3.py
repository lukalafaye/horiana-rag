import openai
from dotenv import load_dotenv
import os
from rag.utils import validate_params

docker = False 

def connect_to_llama3_server():
    chroma_env = '.chroma_env'
    if docker:
        chroma_env = '/app/' + chroma_env
    
    load_dotenv(chroma_env)
    base_url= os.getenv("BASE_URL")
    api_key = os.getenv("API_KEY")

    client = openai.OpenAI(
        base_url=base_url,
        api_key=api_key
    )

    return client 

@validate_params
def request_completion(client, content):
    completion = client.chat.completions.create(
        model="Meta-Llama-3-70B-Instruct",
        messages=[
            {"role": "user", "content": content}
        ]
    )

    print(completion.choices[0].message)

def main():
    client = connect_to_llama3_server()
    content = "What are the primary differences in pathophysiology and treatment approaches between Type 1 and Type 2 diabetes mellitus, and how do these differences impact long-term management strategies for each condition?"
    request_completion(client, content)

if __name__ == "__main__":
    main()
