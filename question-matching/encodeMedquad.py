from sentence_transformers import SentenceTransformer
""" Creates a file where each line is a SentenceTransformer encoding of a respective line from the input file
"""


def encodeMedquad(input_file, output_file, model):
    """ Usage:
            encodeMedquad("medquad-standardized.txt", "encodings-standardized.txt", "FremyCompany/BioLORD-2023")
    """
    model = SentenceTransformer(model)

    read_file = open(input_file, "r")
    read_file_size = len(read_file.readlines())

    read_file = open(input_file, "r")
    write_file = open(output_file, "a")
    write_file.write("Question, Encoding\n")
    
    counter = 0.0
    for line in read_file:
        print("Current progress: ", counter / read_file_size)
        counter += 1
        line = line.split(",")[0]
        if line != "Question":
            embedding = model.encode(line)
            write_file.write(line)
            write_file.write(",")
            write_file.write(str(embedding).replace("\n",""))
            write_file.write("\n")