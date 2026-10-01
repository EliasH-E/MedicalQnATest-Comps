import os
# stupid program that should consolidate all the question and answer files in a folder into a single file!

is_question = False
is_answer = False

write_file = open("consolidated.txt", "a")
write_file.write("Question, Answer\n")

for folder in os.listdir():
    if not os.path.isdir(folder):
        continue
    for file_name in os.listdir(folder):
        if not file_name.endswith(".xml"):
            continue

        read_file = open(folder + "/" + file_name)
        for line in read_file:
            line = line.replace(',', '')
            line = line.replace('\n', ' ')

            if "<Question qid=" in line:
                is_question = True
                line = "".join(line.split('">')[1:])
            if is_question:
                if "</Question>" in line:
                    line = "".join(line.split('</Question>')[:-1])
                    write_file.write(line)
                    is_question = False
                    write_file.write(",")
                else:
                    write_file.write(line)


            if "<Answer>" in line:
                is_answer = True
                line = "".join(line.split("<Answer>")[1:])
            if is_answer:
                print("hi")
                if "</Answer>" in line:
                    is_answer = False
                    line = "".join(line.split("</Answer>")[:-1])
                    write_file.write(line)
                    write_file.write("\n")
                else:
                    write_file.write(line)


