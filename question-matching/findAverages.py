#instead of probabilities these should all say "similarities". oops!
correct_probabilities = open("correct-probabilities.txt", "r")
wrong_probabilities = open("wrong-probabilities.txt", "r")

total_correct_lines = 0
correct_probabilities_sum = 0
total_wrong_lines = 0
wrong_probabilities_sum = 0

for line in correct_probabilities:
    total_correct_lines += 1
    correct_probabilities_sum += float(line)

for line in wrong_probabilities:
    total_wrong_lines += 1
    wrong_probabilities_sum += float(line)

correct_average = correct_probabilities_sum/total_correct_lines
wrong_average = wrong_probabilities_sum/total_wrong_lines
print (correct_average)
print (wrong_average)

correct_probabilities = open("correct-probabilities.txt", "r")
wrong_probabilities = open("wrong-probabilities.txt", "r")

correct_square_sum = 0
wrong_square_sum = 0

for line in correct_probabilities:
    correct_square_sum += (float(line)-correct_average)**2
    

for line in wrong_probabilities:
    wrong_square_sum += (float(line)-wrong_average)**2

correct_stdev = (correct_square_sum/(total_correct_lines-1)) ** .5
wrong_stdev = (wrong_square_sum/(total_wrong_lines-1)) ** .5

print(correct_stdev)
print(wrong_stdev)