from sentence_transformers import SentenceTransformer
sentences = ["Cat scratch injury", "Cat scratch disease", "Bartonellosis"]

model = SentenceTransformer('FremyCompany/BioLORD-2023')
embeddings = model.encode(sentences)
print(embeddings)

write_file = open("encodings-standardized.txt", "a")
write_file.write("Question, Encoding\n")

read_file = open("medquad-standardized.txt", "r")
counter = 0
print(len(read_file.readlines()))

read_file = open("medquad-standardized.txt", "r")
for line in read_file:
    print(counter / 47442)
    counter += 1
    line = line.split(",")[0]
    if line != "Question":
        embedding = model.encode(line)
        write_file.write(line)
        write_file.write(",")
        write_file.write(str(embedding).replace("\n",""))
        write_file.write("\n")