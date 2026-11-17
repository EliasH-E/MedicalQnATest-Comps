# Alexei, Elias, Emma, Daya, Klaus, and Nathan's CS comps :D

We created a pipeline of algorithms to provide simple, medically accurate answers to some patients' questions.

The pipeline:
1. Standardize user input to match database vernacular
2. Create an embedding of the user input and compare that to existing embeddings in our database
3. Match a corresponding question from the MedQuad database. If none exists, prompt the user to try another question.
4. Extract a matching answer to the question.
5. Lexically simplify the answer.
6. Ensure that the simplified answer is grammatically correct.
7. Evaluate the medical accuracy and readability of the simplified answer
8. If not simple enough, repeat steps 5-7 up to 3 times.
9. Output a simplified medically correct answer. 

# Operation

If running for the first time: make sure you have these packages
language_tool_python: pip install language_tool_python
nltk: pip install nltk
    Then in python, run:
      >>> import nltk
      >>> nltk.download('punkt_tab')
pandas: pip install pandas

To run, enter into terminal: python3 main.py