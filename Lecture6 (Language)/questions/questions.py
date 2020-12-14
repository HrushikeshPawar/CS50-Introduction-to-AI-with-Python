import nltk
import sys
import os
import string
from math import log

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    
    # Create a dictionary to store documents
    documents_data = dict()

    # Load files in the directory and add to dictionary
    for dirpath, dirname, filename in os.walk(directory):
        for document in filename:
            doc = open(os.path.join(dirpath, document), "r")
            documents_data[document] = doc.read()

    return documents_data


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    
    # Initialize required lists
    words = nltk.word_tokenize(document.lower())
    remove_words = list()

    # Check every word in the document
    for word in words:

        # Check if word is a stopwords
        if word in nltk.corpus.stopwords.words("english"):
            remove_words.append(word)
        
        # Check if word is a punctuation
        elif (word in string.punctuation) or (word == "=="):
            remove_words.append(word)
        

    # Remove all remove_words from the list "words"
    for word in remove_words:
        words.remove(word)

    # Return the remaining words
    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    
    # Collect all words in the a single list
    all_words = list()

    # Loop through all the documents
    for filename in documents:

        # Add all words in document in list "all_words"
        for word in documents[filename]:
            all_words.append(word)

    # Get all unique words in the "all_words"
    unique_words = set(all_words)

    # IDFs dictionary
    idfs = dict()

    # Calculate the idfs of "unique words"
    for word in unique_words:

        # Initialize the word counter
        cnt = 0

        # Increase the counter if the word appears in the document
        for doc in documents:
            if word in documents[doc]:
                cnt += 1

        # Calculate the Inverse Documnet Frequency
        idfs[word] = log(len(documents.keys()) / cnt)

    # Return the idfs values
    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    
    # Initialize tf_ifds count dic
    tf_idfs = dict()

    # Loop through all documents in files
    for doc in files:

        # Calculate tf-idfs values for all words in query
        score = 0
        for word in query:
            
            # Check if word is in document
            if word not in files[doc]:
                continue

            score += files[doc].count(word) * idfs[word]
        
        # Update the tf-idfs score in dic
        tf_idfs[doc] = score

    # Sort the tf_idfs dic by the scores
    tf_idfs = sorted(tf_idfs.items(), key=lambda x: x[1], reverse=True)

    # Create list of top "n" files
    top_list = list()
    for i in range(n):
        top_list.append(tf_idfs[i][0])
    
    return top_list


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    
    sentences_scores = dict()

    for sentence, words in sentences.items():

        # Words in query
        query_words = list(query)

        # Calculate IDF value of sentences
        idf = 0
        for word in query_words:

            # Skip if word not in sentence
            if word not in words:
                continue
            
            # Update the IDF value of sentence
            idf += idfs[word]

        # Calculate query term density of the sentence
        num_words_in_query = len(query_words)
        query_term_density = num_words_in_query / len(words)

        # Update the sentence score with term density
        sentences_scores[sentence] = {'idf' : idf, 'qtd' : query_term_density}
    
    # Rank the sentence first by IDF then by QTD
    sorted_sentences = sorted(sentences_scores.items(), key=lambda x: (x[1]['idf'], x[1]['qtd']), reverse=True)

    # Return first n terms
    final_list = [sentence[0] for sentence in sorted_sentences]
    return final_list[:n]


if __name__ == "__main__":
    main()
