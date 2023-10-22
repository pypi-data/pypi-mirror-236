import os
import requests
import zipfile
import shutil
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader, PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.docstore.document import Document
import json
import pickle
from bioimageio_chatbot.utils import get_manifest
import yaml

# Read text_files folder to get all txt files including the ones in subfolders
def parse_docs(root_folder, md_separator=None, pdf_separator=None, chunk_size=1000, chunk_overlap=10):
    chunk_list = []
    for foldername, _, filenames in os.walk(root_folder):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                if filename.endswith(".md"):
                    print(f"Reading {file_path}...")
                    documents = TextLoader(file_path).load()
                    text_splitter = CharacterTextSplitter(separator=md_separator or "\n## ", chunk_size=chunk_size, chunk_overlap=chunk_overlap)
                    chunks =text_splitter.split_documents(documents)
                elif filename.endswith(".pdf"):
                    print(f"Reading {file_path}...")
                    documents = PyPDFLoader(file_path).load()
                    text_splitter = RecursiveCharacterTextSplitter(separators=pdf_separator or ["\n\n", "\n", " ", ""], chunk_size=chunk_size, chunk_overlap=chunk_overlap)
                    chunks = text_splitter.split_documents(documents)    
                elif filename.endswith(".txt"):
                    print(f"Reading {file_path}...")
                    documents = TextLoader(file_path).load()
                    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=chunk_size, chunk_overlap=chunk_overlap)
                    chunks = text_splitter.split_documents(documents)
                elif filename.endswith(".json"):
                    # convert json to yaml
                    print(f"Reading {file_path}...")
                    with open(file_path, "r") as json_file:
                        obj = json.load(json_file)
                    yaml_content = yaml.dump(obj)
                    metadata = {"source": file_path}
                    chunks = [Document(page_content=yaml_content, metadata=metadata)]         
                else:
                    print(f"Skipping {file_path}")
                    continue
                chunk_list.extend(chunks)
                    
    return chunk_list

def download_docs(root_dir, url):
    # extract filename from url, remove query string
    filename = url.split("/")[-1].split("?")[0]
    # target directory is ./repos
    target_directory = os.path.join(root_dir, os.path.basename(filename))
    # if the target directory exists, remove it anyway and create a new one
    if os.path.exists(target_directory):
        shutil.rmtree(target_directory)
    os.mkdir(target_directory)
    if filename.endswith(".zip"):
        # Define the file and folder names
        zip_file_name = "main.zip"

        zip_file_path = os.path.join(target_directory, zip_file_name)
        # Download the ZIP file
        response = requests.get(url)
        with open(zip_file_path, "wb") as zip_file:
            zip_file.write(response.content)

        # Unzip the downloaded file 
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            zip_ref.extractall(target_directory)
        # Clean up - remove the downloaded ZIP file
        os.remove(zip_file_path)
        print(f"Downloaded and unzipped {url} to {target_directory}")
    elif filename.endswith(".pdf"):
        response = requests.get(url)
        pdf_file_path = os.path.join(target_directory, filename)
        with open(pdf_file_path, "wb") as pdf_file:
            pdf_file.write(response.content)
        print(f"Downloaded {url} to {target_directory}")
    else:
        raise Exception("Unsupported file format")
    if len(os.listdir(target_directory)) == 0:
        raise Exception("Downloaded folder is empty")
    elif len(os.listdir(target_directory)) == 1:
        # strip the folder name of the unzipped repo
        return os.path.join(target_directory, os.listdir(target_directory)[0])
    # get the folder name of the unzipped repo
    return target_directory


def create_vector_knowledge_base(output_dir=None, collections=None):
    """Create a vector knowledge base from the downloaded documents"""
    if output_dir is None:
        output_dir = os.environ.get("BIOIMAGEIO_KNOWLEDGE_BASE", "./bioimageio-knowledge-base")
    if not collections:
        collections = get_manifest()['collections']
    
    embeddings = OpenAIEmbeddings()
    for collection in collections:
        url = collection['url']
        cached_docs_file = os.path.join(output_dir, collection['id'] + "-docs.pickle")
        if os.path.exists(cached_docs_file):
            with open(cached_docs_file, "rb") as f:
                documents = pickle.load(f)
        else:    
            docs_dir = download_docs(url)
            documents = parse_docs(os.path.join(docs_dir, collection.get('directory', '')))
        if len(documents) > 1000:
            print(f"Waring: only using the first 1000 documents kept for the vector database: {collection['id']}(#documents={len(documents)}))")
            documents = documents[:1000]
        # save the vector db to output_dir
        print(f"Creating embeddings (#documents={len(documents)}))")
        vectordb = FAISS.from_documents(documents, embeddings)
        vectordb.save_local(output_dir, index_name=collection['id'])
        print("Created a vector database from the downloaded documents.")

if __name__ == "__main__":
    create_vector_knowledge_base()