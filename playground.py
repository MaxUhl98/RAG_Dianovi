from vector_database.create import create_vectorstore
from vector_database.update import insert_rows
from datasets import Dataset


data = Dataset.load_from_disk('data/preprocessed_rag_chunks_text_and_heading')
create_vectorstore()
insert_rows(data)