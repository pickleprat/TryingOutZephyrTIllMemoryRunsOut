from langchain.llms import HuggingFacePipeline 
from langchain.chains import LLMChain 
from tqdm.auto import tqdm 
from transformers import pipeline 

from langchain.prompts import (
    PromptTemplate, 
    FewShotPromptTemplate,  
)

from documentloader import (
    splitdocx
)

import os 
import torch 
import warnings 
warnings.simplefilter('ignore')

zephyr_checkpoint = 'HuggingFaceH4/zephyr-7b-beta'

def load_llm(checkpoint, temperature, save_as='Zephyr') : 
    model_path = os.path.join('Models', save_as)
    if os.path.exists(model_path): 
        pipe = pipeline('text-generation', model=model_path,  
                        torch_dtype=torch.bfloat16)
    else:  
        pipe = pipeline("text-generation", model=checkpoint,
                        torch_dtype=torch.bfloat16)
        pipe.save_pretrained(os.path.join('Models', save_as))  

    return HuggingFacePipeline(pipeline=pipe,
                               model_kwargs={'temperature': temperature})
    
def question_answer(split_docx, qnas, temperature=0.05):
  prompt_template = (PromptTemplate
              .from_template("Example {index}\ncontext: {context}\nQNA: {qna}"))

  #load llm locally  
  local_llm = load_llm(zephyr_checkpoint, temperature)

  prompt_prefix = '''You are a question answer generator. Given a certain context,
  generate questions and answers based on that context.
  '''

  examples = [{"index": idx+1, "context": split_docx[idx], "qna": qnas[idx]}
            for idx in range(len(qnas))]

  prompt_format = FewShotPromptTemplate(
      example_prompt=prompt_template,
      prefix=prompt_prefix,
      examples=examples,
      suffix="Context: {context}\nQNA: ",
      input_variables=["context"]
  )

  qnas_for_doc =  []

  llm_chain = LLMChain(prompt=prompt_format, llm=local_llm) 

  progress_bar = tqdm(total=len(split_docx))
  for doc in split_docx:
    qnas_for_doc.append(llm_chain.run(context=doc))
    progress_bar.update(1)

  return qnas_for_doc