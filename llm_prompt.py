from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def generate_answer(query,llm,retriever):
    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the "
        "answer concise."
        "\n\n"
        "{context}"
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{question}"),
        ]
    )

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        |prompt
        |llm
        |StrOutputParser()
    )
    response = rag_chain.stream(query)
    
    return ''.join(response)

# if __name__ == "__main__":
#     load_dotenv()
#     embeddings = HuggingFaceInferenceAPIEmbeddings(
#         api_key=os.environ["HF_API_KEY"], model_name="sentence-transformers/all-MiniLM-l6-v2"
#     )
#     db = Chroma(persist_directory = DB_DIRECTORY, embedding_function= embeddings)
#     llm = ChatMistralAI(model="mistral-large-latest")
#     retriever = db.as_retriever()
#     query = "What are the ways to compute Shapley Value?"
#     print(generate_answer(query))

  

