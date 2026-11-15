
diff_total = 0
total_count = 0


common_total = 0
with open("data_flesch.txt", "r", encoding="utf-8") as file:
    for line in file:
        clean_line = line.strip()  # Removes whitespace and '\n'
        if clean_line:
            split_line = clean_line.split(",")
            diff_total += float(split_line[0])-float(split_line[1])
            common_total += float(split_line[2])-float(split_line[3])
            total_count += 1


print("Flesch",diff_total/total_count)
print("ZipF",common_total/total_count)