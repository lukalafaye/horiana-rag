import openai
from dotenv import load_dotenv
import os
from rag.utils import validate_params

docker = False


def connect_to_llama3_server():
    print(os.getcwd())
    chroma_env = ".llama3_env"
    if docker:
        chroma_env = "/app/" + chroma_env

    load_dotenv(chroma_env)
    base_url = os.getenv("LLAMA_BASE_URL")
    api_key = os.getenv("OPENAI_API_KEY")
    port = os.getenv("LLAMA_PORT")
    model = os.getenv("LLAMA_MODEL")

    if not base_url or not api_key or not port:
        raise ValueError("LLAMA_BASE_URL and OPENAI_API_KEY and LLAMA_PORT must be set")

    print(base_url, port)
    base_url = base_url + ":" + port + "/"
    print(base_url)

    client = openai.OpenAI(base_url=base_url, api_key=api_key)

    return client, model


@validate_params
def request_completion(client, content, model_name):
    completion = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": content}],
    )

    print(completion.choices[0].message)


def main():
    client, model_name = connect_to_llama3_server()
    content = """
    What are the primary differences in pathophysiology and treatment
    approaches between Type 1 and Type 2 diabetes mellitus, and how do
    these differences impact long-term management strategies for each condition?
    """
    request_completion(client, content, model_name)


if __name__ == "__main__":
    main()
