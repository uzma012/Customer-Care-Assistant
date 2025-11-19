from .retriever import Retriever
from .llm import CustomerCareLLM
from .indexer import Indexer

class ChatAssistant:
    def __init__(self):
        self.llm = CustomerCareLLM()
        self.retrieve = Retriever()
        self.system_prompt = """You are a helpful assistant that answers questions using provided context."""
        self.indexer = Indexer()
    def ask(self, query: str, top_k: int = 8, top_n_passages: int = 4):

        retrieved = self.retrieve.retrieve(query)
        prompt = self.retrieve.assemble_prompt(query, self.system_prompt, retrieved[:top_n_passages])
        answer = self.llm.call_llm(prompt)
        return answer, prompt, retrieved[:top_n_passages]