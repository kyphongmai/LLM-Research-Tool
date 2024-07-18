import llm_prompt
import chroma_vector_store
import helper
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_mistralai import ChatMistralAI
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

# Initialising LLM and DB
DB_DIRECTORY = "./chroma_db"
embeddings = HuggingFaceInferenceAPIEmbeddings(
        api_key=os.environ["HF_API_KEY"], model_name="sentence-transformers/all-MiniLM-l6-v2"
    )
db = Chroma(persist_directory = DB_DIRECTORY, embedding_function= embeddings)
llm = ChatMistralAI(model="mistral-large-latest")
retriever = db.as_retriever()

#SIDE BAR
st.sidebar.title("Tell me your pdf folder?")
folder = st.sidebar.text_input("Your Folder")
col1, col2 = st.sidebar.columns(2)
process_clicked = col1.button("Add to database")
delete_clicked = col2.button("Delete database")

if process_clicked:
    pdf_files = helper.list_pdf_files(folder)    
    
    for i, file_path in enumerate(pdf_files):
        file_name_split = file_path.rsplit("/",1)
        file_name = file_name_split[-1]
        st.sidebar.write(f'{i+1}. PROCESSING: "{file_name}"')
        # placeholder.write('processing {file_name}')
        update = chroma_vector_store.build_vector_DB(file_path,db)
        st.sidebar.write(update)

if delete_clicked:
    chroma_vector_store.delete_vectorDB(db)
    st.sidebar.write("Database deleted")

#MAIN PAGE
st.title("""
         Virtual Research Assistant Tool
         Ask me anything
         """)    

query = st.text_input("Question: ")

if query:
    response = llm_prompt.generate_answer(query, llm, retriever)
    st.header("Answer")
    st.subheader(response)



