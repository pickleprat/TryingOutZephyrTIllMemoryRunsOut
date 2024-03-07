# Loading environment variables 
from dotenv import load_dotenv
from langchain.docstore.document import Document 
from huggingface_hub import HfApi 

from documentloader import (
    Docx2txtLoader, 
    clean_text, 
    splitdocx 
)

from SHOTS import (
    QNA_SINGLE, 
    QNA_MULTIPLE
)

import os 

# loading .env files
load_dotenv()

# intializing important constants. 
DATA_PATH = os.getenv("DATA_DIR")
HF_TOKEN = os.getenv("HF_TOKEN")

hf_api = HfApi(
    endpoint='https://huggingface.co', 
    token=HF_TOKEN, 
)

def main():

    # processing the doc
    loader = Docx2txtLoader(DATA_PATH)
    docx_unclean = loader.load()
    docx_content = docx_unclean[0].page_content
    text = clean_text(docx_content)    
    metadata = docx_unclean[0].metadata
    docx = [Document(page_content=text, metadata=metadata)]



if __name__ == '__main__': 
    main()

