from SentenceStandardize import standardize
from medquadComparer import get_closest_q_a
from medquadComparer import get_closest_answer, get_closest_question

user_question = "my eyes are dry. help"

def match_question(user_question):
    standardized_user_question = standardize(user_question)
    print(standardized_user_question)

    closest_answer = get_closest_answer(standardized_user_question)
    print(get_closest_question(standardized_user_question)) #check the matched question
    return closest_answer
print(match_question(user_question))