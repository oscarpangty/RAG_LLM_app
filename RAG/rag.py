from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain.schema.output_parser import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import PromptTemplate
from langchain.vectorstores.utils import filter_complex_metadata
from langchain.schema.runnable import Runnable
    
class ChatPDF:
    vector_store = None
    retriever = None
    chain = None
    
    def __init__(self):
        self.model = ChatOllama(model="llama3")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=100)
        self.prompt = PromptTemplate.from_template(
            """
            <s> [INST] You are an assistant for answering questions. Use the following context elements to answer the question.
            If you do not know the answer, simply say that you do not know. Use a maximum of three sentences and be concise in your response. Don't use words like "context" or "conversation"[/INST] </s>
            [INST] Conversation History: {history}
            Question: {question}
            Context: {context}
            Answer: [/INST]

            """
        )
        
        self.conversation_history = []

    def ingest(self, pdf_file_path: str):
        docs = PyPDFLoader(file_path=pdf_file_path).load()
        chunks = self.text_splitter.split_documents(docs)
        chunks = filter_complex_metadata(chunks)

        vector_store = Chroma.from_documents(documents=chunks, embedding=FastEmbedEmbeddings())
        self.retriever = vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": 3,
                "score_threshold": 0.2,
            },
        )
        self.chain = ({"context": self.retriever, "question": RunnablePassthrough(), "history": RunnablePassthrough()}
                      | self.prompt
                      | self.model
                      | StrOutputParser())

    def ask(self, query: str):
        if not self.chain:
            return "Please, add a PDF document first."

        history_context = "\n".join([f"Question: {q}\nAnswer: {a}" for q, a in self.conversation_history])
        answer = self.chain.invoke({"context": self.retriever, "question": query, "history": history_context})
        self.conversation_history.append((query, answer))
        return answer

    def clear(self):
        self.vector_store = None
        self.retriever = None
        self.chain = None
        self.conversation_history = []
        
        