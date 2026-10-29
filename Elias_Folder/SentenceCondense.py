import spacy
import SentenceSimplify
import NewAndImprovesSentence
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
  print(f"Original: {text}")

  first_result = only_whats_needed(text,importantWords)
  print(f"Simplified: {first_result}")
  final_result = NewAndImprovesSentence.simplify_total_sentence(first_result,importantWords)
  print(f"Simplified: {final_result}")
  return final_result

# Test it out
if __name__ == "__main__":
  text = "The exceptionally quick very lazy brown feline quickly lept over the canine in the citadel."
  #text = "The dauntless wyvern walks towards the tall instructor"
  #text = "The happy man zorts merrily"
  #text = "I like to eat cheese"
  importantWords = set(["lazy"])
  
  simplify(text, importantWords)