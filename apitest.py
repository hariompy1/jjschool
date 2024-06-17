import os

from groq import Groq

client = Groq(
    api_key='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',
)


question ="give list of chapters in class 11 maths book ncert"

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": question,
        }
    ],
    model="llama3-8b-8192",
)

print(chat_completion.choices[0].message.content)