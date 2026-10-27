# Master script for the Medical Questions CS Comps Group
# Written by Klaus Beasley, Elias Hillman-Emelianoff, 
#            Alexei Mendez, Daya Tucker, Emma Yao, Nathan Zhang 

debug = True
# import statements
import language_tool_python

user_input = input("Please enter your question: ")

# correct any user-input grammatical errors
# This step may take a while, need to test
tool = language_tool_python.LanguageTool('en-US')
matches = tool.check(user_input)
user_input = language_tool_python.utils.correct(user_input, matches)
if debug:
    print(f"Corrected user input: {user_input}")

