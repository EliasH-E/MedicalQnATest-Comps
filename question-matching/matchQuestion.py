from SentenceStandardize import standardize
from medquadComparer import get_closest_answer
from medquadComparer import get_closest_q_a

user_question = "how much vitamin b3 should i take?"

def match_question(user_question):
    standardized_user_question = standardize(user_question)
    print(standardized_user_question)

    closest_answer = get_closest_answer(standardized_user_question)

    return closest_answer
print(match_question(user_question))