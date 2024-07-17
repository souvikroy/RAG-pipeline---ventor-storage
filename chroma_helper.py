import pymupdf
import chromadb
import pandas


class Chroma:
    def __init__(self, db_path, collection_name):
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def __read_file(self, path):
        # Reads the pdf file and extracts the text

        file = pymupdf.open(path)
        txt = ''

        for page in file:
            txt += page.get_text()
        return txt, file.name

    def insert_pdf(self, file_path: str, subject="", grade="", chapter=""):
        # Add the provided pdf to Vectorstore

        txt, name = self.__read_file(file_path)

        self.collection.upsert(
            documents=[txt],
            ids=[name],
            metadatas=[{"subject": subject,
                        "grade": grade,
                        "chapter": chapter}]
        )

    def find_questions(self, query_file_path):
        # Retrieve the question from question bank if the chapter is present

        txt, name = self.__read_file(query_file_path)
        results = self.collection.query(
            query_texts=txt,
            n_results=2,  # how many results to return
        )
        distance = results.get("distances", [[1]])[0][0]  # Fetches the distance
        id = results.get("ids", [[""]])[0][0]  # Fetches the record id
        metadata = results.get("metadatas", [[{}]])[0][0]  # Fetches metadata for the record

        if distance < 0.3:
            qbank = pandas.read_csv("QBank.csv")

            questions = qbank[qbank['Name'] == id]  # Filters the questions for particular chapter

            print(f"Question for {id} with {metadata}: ")
            print(questions)

        else:
            print(f"Generating new question for {query_file_path}")
