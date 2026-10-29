read_file = open("medquad-consolidated.txt", "r")
write_file = open("medquad-without-no-answer.txt", "w")
for line in read_file:
    split_line = line.split(",")
    if split_line[1] == "\n":
        continue
    else:
        write_file.write(line)
    