import ollama
import chromadb


prompts = ["从数据中抽取Memory：Mem0首先从提供的文本数据中推断出事实、偏好和记忆。这个过程要求这些事实、偏好和记忆简洁且具有信息性。例如，不是以“这个人喜欢比萨”开始，而是以更直接的“喜欢比萨”来表达。",
         "当新的信息被提供时，Mem0会将其与库中已有的记忆进行合并、更新和组织。这一过程类似于专家合并和更新记忆列表，以确保信息的准确性和最新性。同时，Mem0还会为每项记忆提供与新信息的匹配分数，以便做出明智的决策，决定哪些记忆需要更新或合并。"
           ]
idx = 0

client = chromadb.Client()
collection = client.create_collection('docs')

def add(prompt, idx):
    response = ollama.embeddings(model="shaw/dmeta-embedding-zh", prompt=prompt)
    print(response)
    collection.add(
        ids=[str(idx)],
        embeddings=[response['embedding']],
        documents=[prompt]
    )


for i in prompts:
    add(i, idx)
    idx+=1

q = 'mem0是什么'
response = ollama.embeddings(model="shaw/dmeta-embedding-zh", prompt=q)
res = collection.query(query_embeddings=[response['embedding']], n_results=3)
print(res)
print(res['documents'][0][0])
