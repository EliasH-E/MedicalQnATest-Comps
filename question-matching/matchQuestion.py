from SentenceStandardize import standardize
from medquadComparer import get_closest_answer

user_question = "how much vitamin b3 should i take?"

standardized_user_question = standardize(user_question)
print(standardized_user_question)

closest_answer = get_closest_answer(standardized_user_question)

print(closest_answer)