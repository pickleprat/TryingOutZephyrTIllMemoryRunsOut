import locale, os 
import re 
from langchain_community.document_loaders import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

locale.getpreferredencoding = lambda : "UTF-8"
overlap=30

def clean_text(text_doc):
  pattern = re.compile(r'[\n\t\r]+')
  new_text = re.sub(pattern, ' ', text_doc)
  return new_text

def splitdocx(docx, chunk_size, overlap=overlap): 
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, 
        overlap=overlap, 
        is_separator_regex=False
    )
    split_docx = text_splitter.create_documents([])
    return split_docx


    