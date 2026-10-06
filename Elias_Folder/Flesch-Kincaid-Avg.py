import textstat
import xml.etree.ElementTree as ET
import os


#Average Flesch-Kincaid score of dataset is 11.4

folders = ["1_CancerGov_QA","2_GARD_QA","3_GHR_QA","4_MPlus_Health_Topics_QA","5_NIDDK_QA","6_NINDS_QA","7_SeniorHealth_QA","8_NHLBI_QA_XML","9_CDC_QA"]
folder_path = "../MedQuAD/"

total_files = 0
total_readability = 0
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
                    question = QA.find('Question')
                    
                    if(not question.text):
                        continue
                    total_files += 1
                    print(total_files)
                    total_readability += textstat.flesch_kincaid_grade(question.text)
                    answer = QA.find('Answer')
                    if(not answer.text):
                        continue
                    total_files += 1
                    total_readability += textstat.flesch_kincaid_grade(answer.text)
print(total_readability/total_files)


    