read_file = open("encodings-standardized.txt", "r")
counter = 0
file_num = 1
print(len(read_file.readlines()))
read_file = open("encodings-standardized.txt", "r")
write_file = open("encodings-standardized-1.txt", "a")
for line in read_file:
    print(counter / 8500)
    counter += 1

    write_file.write(line)
    if counter >= 8500:
        counter = 0
        file_num += 1
        write_file = open("encodings-standardized-" + str(file_num) + ".txt", "a")