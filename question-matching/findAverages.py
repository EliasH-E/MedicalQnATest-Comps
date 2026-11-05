


def findSimilarityData(correct_similarities_file, incorrect_similarities_file):
    """ Usage:
            similarity_data = findAverages("correct-similarities.txt", "incorrect-similarities.txt")
    """
    correct_similarities = open(correct_similarities_file, "r")
    incorrect_similarities = open(incorrect_similarities_file, "r")

    total_correct_lines = 0
    correct_similarities_sum = 0
    for line in correct_similarities:
        total_correct_lines += 1
        correct_similarities_sum += float(line)

    total_incorrect_lines = 0
    incorrect_similarities_sum = 0
    for line in incorrect_similarities:
        total_incorrect_lines += 1
        incorrect_similarities_sum += float(line)

    correct_similarities = open(correct_similarities_file, "r")
    incorrect_similarities = open(incorrect_similarities_file, "r")

    correct_average = correct_similarities_sum/total_correct_lines
    correct_square_sum = 0
    for line in correct_similarities:
        correct_square_sum += (float(line)-correct_average)**2

    incorrect_average = incorrect_similarities_sum/total_incorrect_lines
    incorrect_square_sum = 0
    for line in incorrect_similarities:
        incorrect_square_sum += (float(line)-incorrect_average)**2

    correct_stddev = (correct_square_sum/(total_correct_lines-1)) ** .5
    incorrect_stddev = (incorrect_square_sum/(total_incorrect_lines-1)) ** .5

    return {"correct_average": correct_average, "incorrect_average": incorrect_average, "correct_stddev": correct_stddev, "incorrect_stddev": incorrect_stddev}