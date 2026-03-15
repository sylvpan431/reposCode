import os
from openai import OpenAI

client = OpenAI(
    api_key="xxx",
    base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": """你现在扮演一个青少年心理专家的角色，回答问题时要尽可能避免使用专业、晦涩的词汇，要用通俗易懂的语言回答问题。回答问题时，以json格式输出。
                    例如：EXAMPLE INPUT: Which is the highest mountain in the world? Mount Everest.
                    EXAMPLE JSON OUTPUT:
                    {
                        \"question\": \"Which is the highest mountain in the world?\",
                        \"answer\": \"Mount Everest\"
                    }"""},
        {"role": "user", "content": "基本信息：男孩，13岁，初中二年级。虽然知道计划安排未来的事情非常重要，但还是不愿意做这件事情，导致好多作业被遗忘、该做得体育锻炼事项也没做。问题根源是什么？如何解决？"},
    ],
    stream=False
)

print(response.choices[0].message.content)