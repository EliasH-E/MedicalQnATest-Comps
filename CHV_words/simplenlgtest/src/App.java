/*
Run with: 
javac -cp "lib/*" src/App.java
java -cp "src:lib/*" App
*/

import simplenlg.framework.*;
import simplenlg.lexicon.*;
import simplenlg.realiser.english.*;
import simplenlg.phrasespec.*;
import simplenlg.features.*;
import java.util.Arrays;

public class App {
    public static void main(String[] args) {

       // Lexicon lexicon = Lexicon.getDefaultLexicon();
        String DB_FILENAME = "HSqlDb/lexAccess2023.data";
        Lexicon lexicon = new NIHDBLexicon(DB_FILENAME);

        NLGFactory nlgFactory = new NLGFactory(lexicon);
        Realiser realiser = new Realiser(lexicon);

        // eventually want to take in a list of words/phrases and string them together coherently, 
        // and when it encounters punctuation it creates a new document element. but for now this is what it is.
        /* 
        SPhraseSpec p1 = nlgFactory.createClause("s1", "s2", "s3", ...); //add whatever
        SPhraseSpec p2 = nlgFactory.createClause("s1", "s2", "s3", ...); //add whatever
        SPhraseSpec p3 = nlgFactory.createClause("s1", "s2", "s3", ...); //add whatever

        DocumentElement s1 = nlgFactory.createSentence(p1);
        DocumentElement s2 = nlgFactory.createSentence(p2);
        DocumentElement s3 = nlgFactory.createSentence(p3);

        DocumentElement par1 = nlgFactory.createParagraph(Arrays.asList(s1, s2, s3));

        String output = realiser.realise(par1).getRealisation();
        System.out.println(output);
        */
        //SPhraseSpec p = nlgFactory.createClause("patient", "present", "with severe chest pain");

        SPhraseSpec p2 = nlgFactory.createClause("Adult acute myeloid leukemia", "be", "a type of cancer");
        SPhraseSpec p3 = nlgFactory.createClause("the bone marrow", "makes", "abnormal myeloblasts");

        DocumentElement s1 = nlgFactory.createSentence(p2);
        DocumentElement s2 = nlgFactory.createSentence(p3);
        
        DocumentElement par1 = nlgFactory.createParagraph(Arrays.asList(s1, s2));

        String output = realiser.realise(par1).getRealisation();
        System.out.println(output);
        

    }
}