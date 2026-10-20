from sentence_transformers import SentenceTransformer
import numpy as np

def get_closest_answer(user_question):

    model = SentenceTransformer('FremyCompany/BioLORD-2023')
    read_file = open("encodings-standardized-1.txt", "r")
    print("User Question: " + user_question + "\n")
    userQ_embedding = model.encode(user_question)

    max_similarity = 0
    max_question = ""

    counter = 0
    for line in read_file:
        if counter == 0:
            counter += 1
        else:
            embedding_line = line.split(",")[1][1:-2]
            embedding_line = ','.join(embedding_line.split())
            # print(line.split(",")[0])
            restored_embedding = np.fromstring(embedding_line, sep=",")
            similarities = model.similarity(userQ_embedding.astype(np.float64), restored_embedding.astype(np.float64))
            # print(similarities[0][0].item())
            if similarities[0][0].item() > max_similarity:
                max_similarity = similarities[0][0].item()
                max_question = line.split(",")[0]
                # print(max_similarity)
                # print(max_question)
                # print()

    chosen_answer = "ERROR"
    read_file = open("medquad-standardized.txt", "r")
    for line in read_file:
        line = line.split(",")
        q = line[0]
        a = line[1]
        if q == max_question:
            chosen_answer = a
            print(q)
            print(a)
            break
    return chosen_answer
    