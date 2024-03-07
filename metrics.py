from evaluate import load 

# a module  to get the score results 

def reformat(result):
    questions, answers, contexts = [], [], []
    for _, qac_item in enumerate(result): 
        questions.append(qac_item['question'])     
        answers.append(qac_item['answer'])
        contexts.append(qac_item['contexts'])
        
    return questions, answers, contexts 
    

def compute_rquge(questions, contexts, answers):
  rqugescore = load("alirezamsh/rquge")
  results = rqugescore.compute(generated_questions=questions,
                               contexts=contexts, answers=answers)
  return results