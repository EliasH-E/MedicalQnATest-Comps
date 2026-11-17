from sentence_transformers import SentenceTransformer
import numpy as np

""" Set of functions that look through a q/a file for the closest match to an input string, 
    then return some quality of that match

    The input file must be in form "[question],[answer]\n..."
    The user question is matched to some [question]
"""

model = SentenceTransformer('FremyCompany/BioLORD-2023')

def get_closest_question(user_question, qa_file):
    return get_closest_q_a(user_question, qa_file)["question"]

def get_closest_questions_similarity(user_question, qa_file):
    return get_closest_q_a(user_question, qa_file)["similarity"]

def get_closest_answer(user_question, qa_file):
    return get_closest_q_a(user_question, qa_file)["answer"]

def get_closest_q_a(user_question, qa_file):
    """ Input: user question (string), name of formatted medquad file (string)
        Output: dictionary holding the question of maximum similarity (string) to the user question,
                                   the question's answer (string),
                                   and the similarity (from sentencetransformer, float) between the questions
    """
    read_file = open(qa_file, "r")
    userQ_embedding = model.encode(user_question)

    max_similarity = 0
    max_question = ""

    for line in read_file:
        # this segment removes commas from the answer for some reason, may need to reevaluate
        embedding_line = line.split(",")[1][1:-2] 
        embedding_line = ','.join(embedding_line.split()) 
        restored_embedding = np.fromstring(embedding_line, sep=",")

        similarities = model.similarity(userQ_embedding.astype(np.float64), restored_embedding.astype(np.float64))
        if similarities[0][0].item() > max_similarity:
            max_similarity = similarities[0][0].item()
            chosen_question = line.split(",")[0]
            chosen_answer = line.split(",")[1]

    return {"question": chosen_question, "answer": chosen_answer, "similarity": max_similarity}