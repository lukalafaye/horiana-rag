from langchain_core.prompts import ChatPromptTemplate
 
template = ChatPromptTemplate([
    ("system", "You are an AI assistant that helps with daily tasks."),
    ("user", "What's the weather like today?"),
    ("system", "The weather is sunny and warm."),
    ("user", "Should I wear sunscreen?"),
    ("system", "Yes, it's always a good idea to wear sunscreen when it's sunny.")
])
 
print(template.format_messages())