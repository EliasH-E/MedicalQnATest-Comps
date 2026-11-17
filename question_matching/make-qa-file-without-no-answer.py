"""takes file of lines of question-answer pairs and removes the lines with empty answers"""

def makeQAFileWithoutNoAnswer(input_file, output_file):
    """ Input: input file name (string), output file name (string)
        Output: none
    """
    read_file = open(input_file, "r")
    write_file = open(output_file, "w")
    
    for line in read_file:
        split_line = line.split(",")
        if split_line[1] == "\n":
            continue
        else:
            write_file.write(line)
        