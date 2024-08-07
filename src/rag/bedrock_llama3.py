# Use the Converse API to send a text message to Llama 3 Chat 8B.

import boto3
from botocore.exceptions import ClientError

def run():
    # Create a Bedrock Runtime client in the AWS Region you want to use.
    client = boto3.client("bedrock-runtime", region_name="us-east-1")

    # Set the model ID, e.g., Titan Text Premier.
    model_id = "meta.llama3-8b-instruct-v1" # meta.llama3-70b-instruct-v1

    # Start a conversation with the user message.
    user_message = """[INST]You are a a very intelligent bot with exceptional critical thinking[/INST]
    I went to the market and bought 10 apples. I gave 2 apples to your friend and 2 to the helper. I then went and bought 5 more apples and ate 1. How many apples did I remain with?

    Let's think step by step."""
    conversation = [
        {
            "role": "user",
            "content": [{"text": user_message}],
        }
    ]


    try:
        # Send the message to the model, using a basic inference configuration.
        response = client.converse(
            modelId="meta.llama3-8b-instruct-v1:0",
            messages=conversation,
            inferenceConfig={"maxTokens":512,"temperature":0.5,"topP":0.9},
            additionalModelRequestFields={}
        )

        # Extract and print the response text.
        response_text = response["output"]["message"]["content"][0]["text"]
        return response_text

    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        exit(1)


if __name__ == "__main__":
    run()
