from langchain_community.embeddings.openai import OpenAIEmbeddings
#from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.vectorstores import FAISS
#from pydantic import BaseModel
from PyPDF2 import PdfReader
import streamlit as st

class PDFBot:

    version: float = 0.01
    openai_key: str = None

    def __init__(self) -> None:
        self.openai_key = st.secrets.openai['key']


    def get_vectorstore(self, text_chunks):
        embeddings = OpenAIEmbeddings(openai_api_key=self.openai_key)
        vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
        return vectorstore


    def get_pdf_text(self, pdf_docs):
        text = ""
        for pdf in pdf_docs:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text


    def get_text_chunks(self, text):
        text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len)
        chunks = text_splitter.split_text(text)
        return chunks


    def get_conversation_chain(self, vectorstore):
        llm = ChatOpenAI(temperature=0.3, openai_api_key=self.openai_key)
        memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(),
            memory=memory)
        return conversation_chain
    

def main():
    b = PDFBot()



if __name__ == "__main__":
    main()
