from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "{system}"),
        ("user", "{details}"),
    ]
)