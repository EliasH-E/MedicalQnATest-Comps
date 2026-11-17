# Master script for the Medical Questions CS Comps Group
# Written by Klaus Beasley, Elias Hillman-Emelianoff, 
#            Alexei Mendez, Daya Tucker, Emma Yao, Nathan Zhang 

# If running for the first time: make sure you have these packages
# language_tool_python: pip install language_tool_python
# nltk: pip install nltk
#     Then in python, run:
#       >>> import nltk
#       >>> nltk.download('punkt_tab')
# pandas: pip install pandas

# To run, enter into terminal: python3 main.py

debug = True
# import packages
import language_tool_python

#import our functions
from SentenceStandardize import sentenceStandardizer
from question_matching import matchQuestion
from Emma_folder import evaluation
from Simplify_Scripts import CompleteSimplify

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
original_answer = matchQuestion.match_question(user_input)
#closest_question = question_matching["question"]
#original_answer = question_matching["answer"]
#if debug:
##    print(f"Closest question: {closest_question}")
 #   print(f"Closest answer: {original_answer}")

# Standardize answer
answer = sentenceStandardizer(original_answer)

#Simplify answer
answer = SentenceSimplify.CompleteSimplify(answer)
if debug:
    print(f"Standardized+Simplified Answer: {answer}")

# Check coherence
# needs to be implemented

# Evaluate Difficulty
evaluation = evaluation.evaluate_readability(original_answer, answer)
if debug:
    print(f"Flesch-Kincaid before: {evaluation[0]}")
    print(f"Flesch-Kincaid after: {evaluation[1]}")
    
# simplify further if needed

print(answer)