import spacy
import SentenceSynonymReplacer
from GetMedicalText import get_medical_phrases

import med_synonyms
nlp = spacy.load("en_core_web_sm")


def only_whats_needed(text, imporant_words):
  doc = nlp(text)

  # Define what we want to REMOVE (the fluff / optional modifiers)
  drop_deps = {
      "amod"  # Adjectives ("quick", "lazy", "heavy")
  }

  maybe_drop = {
    "advmod"  # Adverbs ("exceptionally", "quickly", "very") but also ("ago" and "notwithstanding") - but we might want those
  }

  # Keep everything EXCEPT the drop list, and some adverbs
  kept_tokens = []
  for token in doc:
    if(token.text in imporant_words):
        kept_tokens.append(token)
    else:
        if(token.dep_ not in drop_deps):
            if(token.dep_ in maybe_drop):
                if(token.text[-1] != "y"):
                    kept_tokens.append(token)
            else:
                kept_tokens.append(token)

  result = ""
  for token in kept_tokens:
    if token.is_punct and result:
      result = result.rstrip() + token.text + " "
    else:
      result += token.text + " "

  return result.strip().capitalize()



def simplify(text, importantWords):
  

  first_result = only_whats_needed(text,importantWords)
  print(f"Simplified: {first_result}")
  final_result = SentenceSynonymReplacer.simplify_total_sentence(first_result,importantWords)
  print(f"Simplified: {final_result}")
  return final_result

# Test it out
if __name__ == "__main__":
  text = "The exceptionally quick very lazy brown feline quickly lept over the canine in the citadel."
  #text = "The dauntless wyvern walks towards the tall instructor"
  #text = "The happy man zorts merrily"
  #text = "I like to eat cheese"
  text = "The patient has muscular atrophy"
  #text = "After Kaposi sarcoma has been diagnosed, tests are done to find out if cancer cells have spread to other parts of the body. The following tests and procedures may be used to find out if cancer has spread to other parts of the body:"
  #text = "What causes abetalipoproteinemia? Abetalipoproteinemia is caused by changes (mutations) in the MTTP gene. The MTTP gene gives the body instructions to make a protein needed for creating beta-lipoproteins. These lipoproteins are necessary for the body to absorb fats, cholesterol, and fat-soluble vitamins (vitamins A, D, E and K), and for transporting these substances in the blood. Mutations in the MTTP result in a lack of beta-lipoproteins, leading to an inability to absorb and transport these substances. This in turn leads to the nutritional and neurologic problems in affected people."
  #text = "this in turn leads to the nutritional and neurologic problems in affected people."
  
  
  print(f"Original: {text}")
  importantWords = set(["lazy"])
  med_result = med_synonyms.med_simple(text)
  text = med_result[0]
  print("Medical Simplifed:",text)
  print()
  importantWords = med_result[1]
  print("Important Words:", importantWords)
  print()
  simplify(text, importantWords)