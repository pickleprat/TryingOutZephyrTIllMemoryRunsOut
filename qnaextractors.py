import re 

def get_qna_multiple(split_docx, result):

  res_multiple = []
  for idx, qna in enumerate(result):
    question_answer_pattern = re.compile(
        r"Question (\d+): (.+?)\nAnswer: (.+?)(?=(Question \d+|$))", re.DOTALL)

    matches = question_answer_pattern.findall(qna)

    for _, qa in enumerate(matches):
      if not qa: continue
      res_multiple.append({
          "question": qa[1].strip(),
          "answer": qa[2].strip(),
          "context": split_docx[idx],
      })

  return res_multiple

def get_qna_single(split_docx, result):

  qac = []
  q_pattern = re.compile(r'Question: (.+?)\n', re.DOTALL)
  a_pattern = re.compile(r'Answer: (.+?)$', re.DOTALL)

  for idx, context in enumerate(split_docx):
    q_match = q_pattern.search(result[idx])
    a_match= a_pattern.search(result[idx])

    qac.append({
        "question": q_match.group(1) if q_match else None,
        "answer": a_match.group(1) if a_match else None,
        "context": context.page_content,
    })

  return qac