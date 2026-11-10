""" Splits a file that's too big to push onto github into multiple files
"""

def splitBigFile(input_file):
    """ Input: input file name (string)
        Output: none
    """
    read_file = open(input_file, "r")
    counter = 0
    file_num = 1

    read_file = open(input_file, "r")
    write_file = open(input_file + "-1.txt", "a")
    for line in read_file:
        counter += 1

        write_file.write(line)
        if counter >= 8500: # 8500 is an arbitrary value
                            # I'm using it because I know 8500 lines of medquad is below the github size limit 
            counter = 0
            file_num += 1
            write_file = open(input_file + "-" + str(file_num) + ".txt", "a")