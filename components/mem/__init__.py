from component import Component
import ollama
import chromadb

comp_name = 'mem'
comp_version = 0
comp_dependency = []
comp_system = '''
You are a people who easily forgot things. When you finish your work, you will forgot everything you do.
Thus you have to record what you do with 'mem'.
For example, you create a file named '1.txt' at desktop, call:
"mem.memory": [
    {"content": "I saved 1.txt at desktop"}
]
After that, when you want to find where did you save the file, call:
"mem.query": [
    {"question": "where is 1.txt?"}
]
Then, you will receive the result.
'''


class Mem:
    def __init__(self, name: str, path: str = None, embedding: str = 'shaw/dmeta-embedding-zh'):
        self.name = name
        self.path = path
        self.embedding_model = embedding
        self.component = Component(comp_name, comp_version, comp_system, comp_dependency)

        # init chroma
        if path is not None:
            client = chromadb.PersistentClient(path=self.path)
            self.collection = client.get_or_create_collection(name=name)
        else:
            self.collection = chromadb.Client().create_collection(name=name)

        # init component
        @self.component.command(
            code='memory',
            usage='remember things',
            arguments={'content': 'things you want to remember'}
        )
        def memory(args):
            self.add(args['content'])

        @self.component.command(
            code='query',
            usage='query things you remember',
            arguments={'question': 'memory that you want to query'},
            result={
                'question': 'memory that you want to query',
                'answer': ['list that contain relative memories'],
            }
        )
        def query(args):
            results = self.query(args['question'])
            return {
                'question': args['question'],
                'answer': results,
            }

    def embed(self, content: str) -> list:
        return ollama.embeddings(model=self.embedding_model, prompt=content)['embedding']

    def add(self, content: str):
        embed = self.embed(content)
        self.collection.add([str(self.collection.count())], [embed])

    def query(self, content: str):
        embed = self.embed(content)
        result = self.collection.query(query_embeddings=[embed], n_results=1)
        return result['documents'][0]
