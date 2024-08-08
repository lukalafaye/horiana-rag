from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate

from src.healthdraft.rag.prompt_setup import (
    create_final_prompt,
)

def create_llama_instance(model_id="meta.llama3-8b-instruct-v1:0"):
    llm = ChatBedrock(
        model_id=model_id,
        model_kwargs=dict(temperature=0),
        region_name="us-east-1"
    )
    return llm

if __name__ == "__main__":
    llm = create_llama_instance()
    print(llm)

    system="You are a medical assistant."
    user="What is asthma?"

    p = create_final_prompt()
    chain = p | llm

    print(chain.invoke({"system": system, "details": user}))

    # !!!! FIX PROMPT LOGIC IN ALL RETRIEVERS LIKE THIS...
