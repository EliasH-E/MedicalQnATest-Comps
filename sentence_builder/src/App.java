
/*
By Daya Tucker

Reconstructs a sentence from token info generated 
by pos_tagger.py. Uses POS tags and dependency 
relationships to construct & realize the sentence.



Run with:

javac -cp "lib/*" src/App.java
java -cp "src:lib/*" App
*/

import simplenlg.framework.*;
import simplenlg.lexicon.*;
import simplenlg.realiser.english.*;
import simplenlg.phrasespec.*;

import java.util.ArrayList;
import java.util.List;

public class App 
{
   
    /*
    Stores info about one token, where a token is a word in the 
    original sentence.
    */
    static class Token 
    {
        String text; // original word as it appears in the sentence
        String pos; // universal part of speech tag
        String lemma; // base form
        String dep; // dependency relationship, i.e., the token's role in relation to its head.
        String head; // word that the token is grammatically connected to
        String headPos; // part of speech of the head word.
        String tag; // more specific POS tag, e.g. singular noun, plural noun, etc.

        Token(String text, String pos, String lemma, String dep, 
        String head, String headPos, String tag)
        {
            this.text = text;
            this.pos = pos;
            this.lemma = lemma;
            this.dep = dep;
            this.head = head;
            this.headPos = headPos;
            this.tag = tag;
        }
    }

    // Expects pipe-delimited output from pos_tagger.py, e.g.
    // word|POS|lemma|dependency|head|head_POS|tag
    //
    // Converts it into a list of Token Objects
    public static List<Token> parseTokens(String input)
    {
        List<Token> tokens = new ArrayList<>();
        String[] lines = input.split("\\r?\\n");

        for (String line : lines)
        {
            line = line.trim();
            if (line.isEmpty())
            {
                continue;
            }

            String[] parts = line.split("\\|", -1);
            if (parts.length == 6 || parts.length == 7)
            {
                String tag = parts.length == 7
                    ? parts[6].trim()
                    : "";
                tokens.add(new Token
                (
                    parts[0].trim(),
                    parts[1].trim(),
                    parts[2].trim(),
                    parts[3].trim(),
                    parts[4].trim(),
                    parts[5].trim(),
                    tag
                ));
            } else{
                System.out.println("Skipping invalid token: " + line);
            }
        }
        return tokens;
    }

    // Finds tokens directly dependent on a particular head
    private static List<Token> findChildren(List<Token> tokens, String head, String dependency) 
    {
        List<Token> children = new ArrayList<>();
        for (Token token : tokens)
        {
            if (token.head.equals(head) && token.dep.equals(dependency))
            {
                children.add(token);
            }
        }
        return children;
    }

    // Creates a noun phrase using noun and dependent tokens,
    // i.e., any words that modify or specify it
    private static NPPhraseSpec createNounPhrase(Token noun, List<Token> tokens,
        NLGFactory factory) 
    {
        NPPhraseSpec phrase = factory.createNounPhrase();

        List<Token> determiners = findChildren(tokens, noun.text, "det");

        if (!determiners.isEmpty()) 
        {
            phrase.setSpecifier(determiners.get(0).text);
        } else {
            phrase.setSpecifier("the");
        }

        List<Token> adjectives = findChildren(tokens, noun.text, "amod");

        for (Token adjective : adjectives) 
        {
            phrase.addPreModifier(adjective.text);
        }

        List<Token> compounds = findChildren(tokens, noun.text, "compound");

        for (Token compound : compounds) 
        {
            phrase.addPreModifier(compound.text);
        }

        phrase.setNoun(noun.text);
        return phrase;
    }

    // constructs the sentence 
    public static String constructSentence(List<Token> tokens, NLGFactory nlgFactory,
        Realiser realiser
    ) 
    {
        // find root of the sentence
        Token root = null;

        for (Token token : tokens) 
        {
            if (token.dep.equals("ROOT")) 
            {
                root = token;
                break;
            }
        }

        if (root == null) 
        {
            return "Unable to construct sentence: no root.";
        }

        // find the subject
        List<Token> subjects = new ArrayList<>();

        for (Token token : tokens) 
        {
            if ((token.dep.equals("nsubj") ||
                 token.dep.equals("nsubjpass")) &&
                token.head.equals(root.text)) 
            {
                subjects.add(token);
            }
        }

        if (subjects.isEmpty()) 
        {
            return "Unable to construct sentence: no subject.";
        }

        NPPhraseSpec subject = createNounPhrase(subjects.get(0), tokens, nlgFactory);

        SPhraseSpec clause = nlgFactory.createClause();
        clause.setSubject(subject);

        // find the main verb + coordinated verbs
        List<Token> verbs = new ArrayList<>();

        if (root.pos.equals("VERB") || root.pos.equals("AUX")) 
        {
            verbs.add(root);
        }

        for (Token token : tokens) 
        {
            if (token.dep.equals("conj") &&
                token.head.equals(root.text) &&
                (token.pos.equals("VERB") ||
                 token.pos.equals("AUX"))) 
            {
                verbs.add(token);
            }
        }

        // use the original forms instead of lemmas
        if (verbs.isEmpty()) 
        {
            clause.setVerb("be");
            clause.setComplement("present");
        } else if (verbs.size() == 1) 
        {
            clause.setVerb(verbs.get(0).text);

        } else 
        {
            CoordinatedPhraseElement coordinatedVerbs = nlgFactory.createCoordinatedPhrase();

            for (Token verb : verbs) 
            {
                coordinatedVerbs.addCoordinate(verb.text);
            }
            clause.setVerb(coordinatedVerbs);
        }

        // Find direct objects
        for (Token token : tokens) 
        {
            if ((token.dep.equals("dobj") ||
                 token.dep.equals("obj")) &&
                token.head.equals(root.text)) 
            {

                NPPhraseSpec object = createNounPhrase(token, tokens, nlgFactory);
                clause.setObject(object);
                break;
            }
        }

        // find prepositional phrases
        for (Token token : tokens) 
        {
            if (!token.dep.equals("prep")) 
            {
                continue;
            }
            boolean belongsToVerb = false;
            for (Token verb : verbs) 
            {
                if (token.head.equals(verb.text)) 
                {
                    belongsToVerb = true;
                    break;
                }
            }
            if (!belongsToVerb) 
            {
                continue;
            }

            List<Token> objects = findChildren(tokens, token.text, "pobj");

            if (objects.isEmpty()) 
            {
                objects = findChildren(tokens, token.text, "obj");
            }
            if (objects.isEmpty()) 
            {
                continue;
            }

            NPPhraseSpec object = createNounPhrase(objects.get(0), tokens, nlgFactory);
            PPPhraseSpec phrase = nlgFactory.createPrepositionPhrase();
            phrase.setPreposition(token.text);
            phrase.addComplement(object);
            clause.addPostModifier(phrase);
        }

        // Add adverbs modifying the main / coordinated verbs
        for (Token token : tokens) 
        {
            if (!token.dep.equals("advmod")) 
            {
                continue;
            }

            for (Token verb : verbs) 
            {
                if (token.head.equals(verb.text)) 
                {
                    clause.addModifier(token.text);
                    break;
                }
            }
        }
        return realiser.realiseSentence(clause);
    }

    public static void main(String[] args) throws Exception 
    {

        String DB_FILENAME = "HSqlDb/lexAccess2023.data";
        Lexicon lexicon = new NIHDBLexicon(DB_FILENAME);
        NLGFactory nlgFactory = new NLGFactory(lexicon);
        Realiser realiser = new Realiser(lexicon);

        // Example input from pos_tagger.py:
        String input =
            "the|DET|the|det|fox|NOUN\n" +
            "and|CCONJ|and|cc|slides|VERB\n" +
            "brown|ADJ|brown|amod|fox|NOUN\n" +
            "fox|NOUN|fox|nsubj|jumps|VERB\n" +
            "jumps|VERB|jump|ROOT|jumps|VERB\n" +
            "and|CCONJ|and|cc|slides|VERB\n" +
            "slides|VERB|slide|conj|jumps|VERB\n" +
            "over|ADP|over|prep|jumps|VERB\n" +
            "the|DET|the|det|dog|NOUN\n" +
            "lazy|ADJ|lazy|amod|dog|NOUN\n" +
            "dog|NOUN|dog|pobj|over|ADP\n" +
            ".|PUNCT|.|punct|jumps|VERB\n";

        List<Token> tokens = parseTokens(input);
        String output = constructSentence(tokens, nlgFactory, realiser);

        System.out.println("Original input:");
        System.out.println(input);
        System.out.println("Constructed sentence:");
        System.out.println(output);
    }
}
