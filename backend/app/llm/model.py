import os

from dotenv import load_dotenv
from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
MODEL = "gpt-4"
TEMPERATURE = 0.1


custom_temp = """
You are a helpful customer assistant with the main aim of helping the customer 
understand the product they are interested in better. You will be answering 
questions based on multiple consumer reviews of a particular product which 
have all been concatenated together into one single text to help understand 
what previous users of the product have said. 

context: {context}
question: {question}

Only return helpful answers below and nothing else. If you do not know the 
answer to the customers question then please state that you don't and try to 
avoid repeating yourself. Concisely answer any questions a customer has.  
"""


def set_custom_prompt():
    prompt = PromptTemplate(
        template=custom_temp, input_variables=["context", "question"]
    )
    return prompt


def get_text_chunks(text: str) -> list[str]:
    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text: str):
    info = get_text_chunks(text=text)
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=info, embedding=embeddings)
    return vectorstore


def load_llm():
    llm = ChatOpenAI(
        openai_api_key=OPENAI_API_KEY, model=MODEL, temperature=TEMPERATURE
    )
    return llm


def retrival_qa_chain(llm, prompt, db):
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=db.as_retriever(search_kwargs={"k": 2}),
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt},
    )
    return chain


def init_ai(text: str):
    db = get_vectorstore(text=text)
    llm = load_llm()
    prompt = set_custom_prompt()
    qa = retrival_qa_chain(llm=llm, prompt=prompt, db=db)
    return qa


def model(text: str, query: str):
    result = init_ai(text=text)
    response = result({"query": query})
    return response
