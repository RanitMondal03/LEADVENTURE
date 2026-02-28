from openai import OpenAI

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key="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"
)

completion = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "user",
            "content": "How many 'a' in huggingface?"
        }
    ]
)

print(completion.choices[0].message.content)