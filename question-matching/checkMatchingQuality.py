from medquadComparer import get_closest_question
from SentenceSimplify import simplify


input_sentences = open("encodings-standardized-1.txt", "r")

correct_count = 0
incorrect_count = 0
total_count = 0

for line in input_sentences:
    sentence = line.split(",")[0]
    simple_sentence = simplify(sentence).replace("be( be)","is")
    closest_question = get_closest_question(simple_sentence)
    # print(simple_sentence)
    # print(get_closest_question(simple_sentence))
    total_count += 1
    if sentence == closest_question:
        correct_count += 1
        # print(sentence, simple_sentence, closest_question)
        # continue
        # print("yay!")
    else:
        incorrect_count += 1
        # print("no!")
    print(correct_count/total_count)