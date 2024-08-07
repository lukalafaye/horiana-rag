from langchain_aws import ChatBedrock

llm = ChatBedrock(
    model_id="meta.llama3-8b-instruct-v1:0",
    model_kwargs=dict(temperature=0),
    region_name="us-east-1"
    # other params...
)

from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant that translates {input_language} to {output_language}.",
        ),
        ("human", "{input}"),
    ]
)

chain = prompt | llm
ai_msg = chain.invoke(
    {
        "input_language": "English",
        "output_language": "German",
        "input": "I love programming.",
    }
)

print(ai_msg.content)
