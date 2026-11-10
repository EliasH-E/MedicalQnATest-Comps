from SentenceStandardize import standardize

""" Uses SentenceStandardize to standardize every line in a file's medical terms and write the result to another file.
    REQUIRES a file of format "[question],[answer]\n" and only standardizes the [question]s 
"""

def standardizeQuestions(input_file, output_file): 
    """ Input: input file name (string), output file name (string)
        Output: none
    """
    read_file = open(input_file, "r")
    write_file = open(output_file, "w")

    counter = 0
    for line in read_file:
        print(counter / 16409) # percentage "done" the program is
        split_line = line.split(",")
        write_file.write(standardize(split_line[0]).replace(",","")) # no commas because question and answer are split by
        write_file.write(",")
        write_file.write(split_line[1])
        counter += 1