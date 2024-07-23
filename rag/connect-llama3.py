import openai

client = openai.OpenAI(
    base_url="http://ec2-XX-XXX-XXX-XX.us-east-2.compute.amazonaws.com:8080/v1/",
    api_key="secret"
)

completion = client.chat.completions.create(
    model="Meta-Llama-3-70B-Instruct",
    messages=[
        {"role": "user", "content": "Hello!s"}
    ]
)

print(completion.choices[0].message)