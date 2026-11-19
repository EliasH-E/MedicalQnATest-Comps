How to compile:
1) Clone the MedQUaD repository
2) Place xml-consolidator.py inside the repository and run it
        It should create a file called "consolidated.txt" of format "[question],[answer]\n"
3) Place consolidated.txt in the question_matching folder
4) Run make-qa-file-without-no-answer.py
        The output file, unless edited, is called "clean-consolidated.txt"
5) Run encodeMedquad.py on the generated file
        It should generate a new file of format "[question],[sentencetransformer embedding of question]\n"
6) Use the two files as inputs for matchQuestion.py

7) Optionally, use splitEncodings.py to split any large files so that they can be pushed to github
        There is not yet a program to put the split files back together