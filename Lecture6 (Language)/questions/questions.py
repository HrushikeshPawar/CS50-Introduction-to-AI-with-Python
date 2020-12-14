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

    print()
    print("All files loaded from the directory.")
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
    print("Tokenization Completed")
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
    print()
    print("Completed Inverse Document Frequency Calculations")
    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    raise NotImplementedError


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
