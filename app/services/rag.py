# import os

# from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_huggingface.embeddings.huggingface import HuggingFaceEmbeddings

persist_directory = "./chroma/machines"

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# load_dotenv()
#
# os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

model = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    max_retries=2,
)

def get_chain():
    sys_prompt = f"""You are an expert on machines that produce caps, and you will receive a question from a user. 
    Your job is to answer the question returning the name and technical details of the best machine among the ones 
    in the context. Don't talk to the user like you have a list in front of you."""

    template = """
    UserInput: {question}.
    
    Context:
    {context}."""

    prompt = PromptTemplate.from_template(sys_prompt + template)
    return prompt | model

def get_embedded_database():
    db = Chroma(persist_directory=persist_directory,
                embedding_function=embeddings)

    return db

def generate_rag_response(question: str) -> str:
    chain = get_chain()
    db = get_embedded_database()
    docs = db.similarity_search_with_score(question, k=5)
    context = ""
    for doc in docs:
        context += 'Name' + doc[0].metadata['name'] + '\n' +  doc[0].page_content

    response = chain.invoke({"question": question, "context": context})
    return response.content
  
