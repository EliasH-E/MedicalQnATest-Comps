from SentenceStandardize import standardize

read_file = open("medquad-without-no-answer.txt", "r")
write_file = open("medquad-standardized.txt", "w")
counter = 0
for line in read_file:
    print(counter / 16409)
    split_line = line.split(",")
    write_file.write(standardize(split_line[0]).replace(",",""))
    write_file.write(",")
    write_file.write(split_line[1])
    # print(standardize(split_line[0]))
    counter += 1