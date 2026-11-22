from .SentenceStandardize import standardize
from .medquadComparer import get_closest_answer, get_closest_question

""" !!MAIN FILE FOR QUESTION MATCHING!!

    Uses medquadComparer to semantically determine the closest question in MedQUaD 
    to a standardized (SentenceStandardizer) version of the input string, 
    then returns MedQUaD's answer to that question
"""

def match_question(user_question, questions_to_answers_file, questions_to_encodings_file):
    """ Input: user question (string)
               file of questions and their SentenceTransformer encodings separated by a comma 
                    in the format "[question],[encoding of question]\n"
               file of questions and their answers
        Output: answer (string)
        Example: print(match_question("What is blood loss?", "medquad-standardized.txt", "encodings-standardized-1.txt"))
    """
    standardized_user_question = standardize(user_question)
    closest_answer = get_closest_answer(standardized_user_question, questions_to_answers_file, questions_to_encodings_file)
    return closest_answer

#print(match_question("What is a blood clot?", "medquad-standardized.txt", "encodings-standardized-1.txt"))