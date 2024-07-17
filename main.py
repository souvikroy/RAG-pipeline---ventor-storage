from chroma_helper import Chroma

# Initialize DB
db_path = "vectordb"
collection_name = "mycollection"
vector_store = Chroma(db_path=db_path, collection_name=collection_name)

# Add a pdf in Vectorstore
vector_store.insert_pdf(
    file_path="lehs2dd/lehs201.pdf",
    subject="History",
    grade="11",
    chapter="2"
)

# Retrieve questions for particular chapter
vector_store.find_questions("lehs2dd/lehs203.pdf")
