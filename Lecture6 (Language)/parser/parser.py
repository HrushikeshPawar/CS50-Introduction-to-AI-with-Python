import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | VP NP | S Conj S

NP -> N | Det N | Det AdjP N | NP PP

VP -> V | V NP | VP Adv | Adv VP | VP PP

AdjP -> Adj | Adj AdjP

PP -> P | P NP
"""
grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)

def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))

def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    
    # Separate sentence in words
    words = nltk.word_tokenize(sentence)

    # Mark non-alphabetic words and make words lower case
    remove_words = list()
    for n, word in enumerate(words):
        if not word.isalpha():
            remove_words.append(word)
        else:
            words[n] = word.lower()
    
    # Remove non-alphabetic words
    for word in remove_words:
        words.remove(word)

    # Return the list of words in given sentence
    return words

def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    
    # Initialize np_chunks
    np_chunks = list()
    
    # Loop through all subtrees
    for subtree in tree.subtrees():

        # Only select nodes with label "NP"
        if subtree.label() == "NP":
            cnt = 0

            # Check if the selected node has a nested "NP" node
            for t in subtree.subtrees():
                if t.label() == "NP":
                    cnt += 1
            
            if cnt < 2:
                np_chunks.append(subtree)
   
    # Return np_chunks
    return np_chunks

if __name__ == "__main__":
    main()
