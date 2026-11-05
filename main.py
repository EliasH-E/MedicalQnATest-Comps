# Master script for the Medical Questions CS Comps Group
# Written by Klaus Beasley, Elias Hillman-Emelianoff, 
#            Alexei Mendez, Daya Tucker, Emma Yao, Nathan Zhang 

debug = True
# import packages
import language_tool_python

#import our functions
from SentenceStandardize import sentenceStandardizer
from ..question-matching import get_closest_q_a


user_input = input("Please enter your question: ")

# Correct any user-input grammatical errors
# This step may take a while, need to test
tool = language_tool_python.LanguageTool('en-US')
matches = tool.check(user_input)
user_input = language_tool_python.utils.correct(user_input, matches)
if debug:
    print(f"Corrected user input: {user_input}")

# Standardize User input
user_input = sentenceStandardizer(user_input)
if debug:
    print(f"Standardized user input: {user_input}")

# Match user input to a question/answer
question_matching = get_closest_q_a(user_input)
closest_question = question_matching["question"]
answer = question_matching["answer"]
if debug:
    print(f"Closest question: {closest_question}")
    print(f"Closest question: {answer}")

# Standardize answer
answer = sentenceStandardizer(answer)

#Simplify answer

# Check coherence

# Evaluate Difficulty
# simplify further if needed

print(answer)