from stemmer import Stemmer

# Program starts here.
if __name__ == '__main__':
    # Instantiate Stemmer object
    my_stemmer = Stemmer()
    # Generate your text
    my_words = my_stemmer.preprocess("test1.txt")
    # Apply stemming to the list of words
    my_words = my_stemmer.stem_words(my_words)

