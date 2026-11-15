import textstat
import xml.etree.ElementTree as ET
import os
import CompleteSimplify
import random

from SentenceSynonymReplacer import normal_avg_zipf
#Average Flesch-Kincaid score of dataset is 11.4

folders = ["2_GARD_QA","3_GHR_QA","4_MPlus_Health_Topics_QA","5_NIDDK_QA","6_NINDS_QA","7_SeniorHealth_QA","8_NHLBI_QA_XML","9_CDC_QA"]
folder_path = "../../../MedQuAD/"

total_files = 0
total_readability = 0
start = 0
with open("data_flesch.txt", "a", encoding="utf-8") as f:
    for i in folders:
        new_path = folder_path + i
        for filename in os.listdir(new_path):
            full_path = os.path.join(new_path, filename)
            if os.path.isfile(full_path):
                #print(full_path)
                tree = ET.parse(full_path)
                root = tree.getroot()
                for QAset in root.findall('QAPairs'):
                    for QA in QAset.findall('QAPair'):
                        
                        answer = QA.find('Answer')
                        if(not answer.text):
                            continue
                        # print(total_files)
                       # if(random.randrange(0,25) != 4):
                        #    continue
                        total_files += 1
                       
                        new_text = CompleteSimplify.complete_simplification(answer.text)
                        oldflesch = textstat.flesch_kincaid_grade(answer.text)
                        newflesch = textstat.flesch_kincaid_grade(new_text)

                        oldcommon = normal_avg_zipf(answer.text)
                        newcommon = normal_avg_zipf(new_text)
                        f.write(str(oldflesch) +","+str(newflesch)+","+str(oldcommon)+","+str(newcommon)+"\n")
                        #print(oldflesch, newflesch)
                        total_readability +=newflesch

    print(total_readability/total_files)


    