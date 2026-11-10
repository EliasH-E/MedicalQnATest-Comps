from medquadComparer import get_closest_question
from medquadComparer import get_closest_q_a
from SentenceSimplify import simplify
from med_synonyms import simplify_term
from med_synonyms import load_chv

""" File that uses medquadComparer, SentenceSimplify, and med_synonyms 
    to match a simplified version of each input question back to its original version. """


def writeSimilaritiesSplitByCorrectness(input_file, correct_output_file, incorrect_output_file):
    """ Writes the similarities of successful and unsuccessful matches to their respective files
        No return value
        Usage:
            writeSimilaritiesSplitByCorrectness("encodings-standardized-1.txt", "correct-similarities.txt", "incorrect-similarities.txt")
    """
    chv = load_chv()
    input_sentences = open(input_file, "r")
    correct_file = open(correct_output_file, "a")
    wrong_file = open(incorrect_output_file, "a")

    for line in input_sentences:
        original_question = line.split(",")[0]
        simple_sentence = simplify_term(simplify(original_question).replace("be( be)","is"), chv) 
                                                                    # simplification can add artifacts like "be( be)"

        closest_data = get_closest_q_a(simple_sentence)

        if original_question == closest_data["question"]:
            correct_file.write(str(closest_data["similarity"]) + "\n")
        else:
            wrong_file.write(str(closest_data["similarity"]) + "\n")


def getMatchingCorrectness(input_file):
    """ Calculates the percentage of correct matches made between sentences and their simplifications. 
        Not very useful due to simplification errors.
        Returns percentage of correct matches and prints updates after every comparison
        Usage:
            percentage_correct = getMatchingCorrectness("encodings-standardized-1.txt")
    """

    chv = load_chv()
    input_sentences = open(input_file, "r")

    correct_count = 0.0
    incorrect_count = 0.0
    total_count = 0.0

    for line in input_sentences:
        original_question = line.split(",")[0]
        simple_sentence = simplify_term(simplify(original_question).replace("be( be)","is"), chv)

        closest_data = get_closest_q_a(simple_sentence)

        total_count += 1
        if original_question == closest_data["question"]:
            correct_count += 1
        else:
            incorrect_count += 1
        print("Correct: ", correct_count, ", Incorrect: ", incorrect_count, ", Percentage Correct: ", correct_count/total_count)
    return correct_count/total_count