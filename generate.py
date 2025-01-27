from langchain import ConversationChain
from langchain.memory import ConversationBufferMemory
from model import *
from function import *
import time

#defects4j
llm = deepseek(api_key="your api-key")
generate_mutant('Chart',0,'./',llm)

llm = StarChat(model_path='path')
generate_mutant('Chart',0,'./',llm)

llm = CodeLlama13B(model_path='path')
generate_mutant('Chart',0,'./',llm)

llm = GPT(api_key="your api-key",model="GPT-3.5-turbo")
generate_mutant('Chart',0,'./',llm)

llm = GPT(api_key="your api-key",model="GPT-4o")
generate_mutant('Chart',0,'./',llm)

llm = GPT(api_key="your api-key",model="GPT-4o-mini")
generate_mutant('Chart',0,'./',llm)

#condefect
llm = deepseek(api_key="your api-key")
con_generate_mutant(llm)

llm = StarChat(model_path='path')
con_generate_mutant(llm)

llm = CodeLlama13B(model_path='path')
con_generate_mutant(llm)

llm = GPT(api_key="your api-key",model="GPT-3.5-turbo")
con_generate_mutant(llm)

llm = GPT(api_key="your api-key",model="GPT-4o")
con_generate_mutant(llm)

llm = GPT(api_key="your api-key",model="GPT-4o-mini")
con_generate_mutant(llm)