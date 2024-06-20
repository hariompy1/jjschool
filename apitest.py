import os

from groq import Groq

client = Groq(
    api_key='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',
)

def ai(question):
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": question,
        }
    ],
    model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content



# question ="give list of chapters in class 11 maths book ncert"

print(ai("write a butiful login page in html and remember css also in html file okay both in one html file both code"))