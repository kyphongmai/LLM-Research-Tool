from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from hashlib import sha256

def generate_id(document_content):
    return sha256(document_content.encode('utf-8')).hexdigest()

def is_document_present(_id, vectorDB):
    return _id in vectorDB.get()['ids']

def update_vectorDB(document,vectorDB):
    ids = [generate_id(doc.page_content) for doc in document]
    if not is_document_present(ids[0],vectorDB):
        vectorDB.add_documents(documents = document, ids =ids)
        response = "...... is being added to the database ✅"
    else: 
        response = "...... already exists in the database ❗️"
    return response

def delete_vectorDB (vectorDB):
    vectorDB.delete_collection()

def build_vector_DB(file_path, vectorDB):    
    #Load file_path
    loader = PyPDFLoader(file_path)
    data = loader.load()

    #Split pdf file into chunks
    splitter = RecursiveCharacterTextSplitter(separators = ["/n",". "],
                                              chunk_size = 1000,
                                              chunk_overlap = 0
                                             )
    chunks = splitter.split_documents(data)

    if not chunks:
        return "...... cannot process ❌"
    #Remove unwanted space from chunks
    for chunk in chunks:
       chunk.page_content = chunk.page_content.replace("\n", " ")
    
    #Update vector
    return update_vectorDB(chunks, vectorDB)


#if __name__ == "__main__":
    # load_dotenv()
    # file_path = "data/pdf/original shapley.pdf"
    # embeddings = HuggingFaceInferenceAPIEmbeddings(
    #                 api_key=os.environ["HF_API_KEY"], 
    #                 model_name="sentence-transformers/all-MiniLM-l6-v2"
    #             )
    # db = Chroma(persist_directory = DB_DIRECTORY, embedding_function= embeddings)
    # build_vector_DB(file_path, db)
    

    