from SentenceStandardize import standardize
from medquadComparer import get_closest_answer, get_closest_question

""" Uses medquadComparer to semantically determine the closest question in MedQUaD 
    to a standardized (SentenceStandardizer) version of the input string, 
    then returns MedQUaD's answer to that question
"""

def match_question(user_question):
    """ Input: user question (string)
        Output: answer (string)
    """
    standardized_user_question = standardize(user_question)
    closest_answer = get_closest_answer(standardized_user_question)
    return closest_answer