from medquadComparer import get_closest_question
from medquadComparer import get_closest_q_a
from SentenceSimplify import simplify
from med_synonyms import simplify_term
from med_synonyms import load_chv


input_sentences = open("encodings-standardized-1.txt", "r")
chv = load_chv()

correct_count = 0
incorrect_count = 0
total_count = 0

for line in input_sentences:
    sentence = line.split(",")[0]
    simple_sentence = simplify_term(simplify(sentence).replace("be( be)","is"), chv)
    # closest_question = get_closest_question(simple_sentence)
    closest_data = get_closest_q_a(simple_sentence)
    if sentence == closest_data["question"]:
        correct_file = open("correct-probabilities.txt", "a")
        correct_file.write(str(closest_data["similarity"]) + "\n")
    else:
        wrong_file = open("wrong-probabilities.txt", "a")
        wrong_file.write(str(closest_data["similarity"]) + "\n")

    closest_question = closest_data["question"]
    # print(simple_sentence)
    # print(get_closest_question(simple_sentence))
    total_count += 1
    # print(sentence, simple_sentence, closest_question)
    if sentence == closest_question:
        correct_count += 1
        # continue
        # print("yay!")
    else:
        incorrect_count += 1
        # print("no!")
    # print(correct_count/total_count)