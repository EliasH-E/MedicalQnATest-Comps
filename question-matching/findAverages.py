""" Finds and returns the averages and standard deviations for each line in a file
    Used initially for finding similarity data
"""


def findAverage(input_file_name):
    """ Inputs: name of file whose lines are integers or floats 
        Outputs: average (float)
        Usage:
            average = findAverage("correct-input_file.txt")
    """
    input_file = open(input_file_name, "r")
    

    total_lines = 0
    input_file_sum = 0
    for line in input_file:
        total_lines += 1
        input_file_sum += float(line)

    input_file = open(input_file_file, "r")

    average = input_file_sum/total_lines

    return average


def findStandardDeviation(input_file_name):
    """ Inputs: name of file whose lines are integers or floats 
        Outputs: standard deviation (float)
        Usage:
            similarity_data = findStandardDeviation("correct-input_file.txt")
    """
    
    average = findAverage(input_file_name)

    input_file = open(input_file_name, "r")

    square_sum = 0
    for line in input_file:
        square_sum += (float(line)-average)**2


    stddev = (square_sum/(total_lines-1)) ** .5

    return stddev