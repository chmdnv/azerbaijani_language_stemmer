import re
from string import punctuation


class Stemmer:
    """Stemmer class definition

    Attributes:
        words : set
            Stores the words loaded from the words.txt file
        suffixes: list
            Stores the suffixes loaded from the suffix.txt file
        stems: list
            Stores all possible stems of a word

    Methods:
        __load_words:
            Loads the words from the word.txt file into memory
        __load_suffixes:
            Loads the suffixes from the suffix.txt file into memory
        preprocess(file)
            Reads and preprocesses input txt file
        converter(word)
            Converts irregular suffixes to regular form
        suffix(word)
            Removes suffix from the word
        stem_word(word)
            Stems and returns stemmed version of the word
        stem_words(list_of_words)
            Stems and returns stemmed versions of all words in the given file

    """
    words = set()
    suffixes = []
    stems = []


    def __init__(self):
        """Constructor of the Stemmer class
        """
        # Loads words from the words.txt file
        self.__load_words()
        # Loads suffixes from the suffix.txt file
        self.__load_suffixes()


    def __del__(self):
        """Destructor of the Stemmer class
        """
        # Clear both lists to free the memory space
        self.words.clear()
        self.suffixes.clear()


    def __load_words(self):
        """Loads the words from the word.txt file into memory
        """
        # Open words.txt file in read mode with utf-8 encoding.
        with open("words.txt", "r", encoding="utf8") as words_file:
            # Iterate over each line in the words.txt file
            for word in words_file:
                # Trim the spaces and newline characters from the string before adding to the list
                self.words.add(word.strip())


    def __load_suffixes(self):
        """Loads the suffixes from the suffix.txt file into memory
        """
        # Open suffix.txt file in read mode with utf-8 encoding
        with open("suffix.txt", "r", encoding="utf8") as suffix_file:
            # Iterate over each line in the suffix.txt file
            for suffix in suffix_file:
                # Trim the spaces and newline characters from the string before adding to the list
                self.suffixes.append(suffix.strip())
        self.suffixes.sort(key=len, reverse=True)

    def preprocess(self, file):
        """Preprocess your text: remove punctuation, replace AZ/EN chars, lowercase the letters, remove special chars,
        trim the spaces and newlines and split the text by space/s
        """
        with open(file, 'r', encoding="utf-8-sig") as text:
            my_text = text.read()

        replace_list = {
            "İ": "i",
            "ü": "u",
            "ə": "e",
            "Ə": "e",
            "ı": "i",
            "ö": "o",
            "ğ": "g",
            "ş": "s",
            "ç": "c",
            "w":"s"
        }
        for key, value in replace_list.items():
            my_text = my_text.replace(key, value)
        my_text = my_text.lower()
        my_text = re.sub('[^a-zA-Z0-9 \n\.]̇', '', my_text)
        for key, value in replace_list.items():
            my_text = my_text.replace(key, value)
        my_text = my_text.split()
        my_words = []
        for word in my_text:
            my_words.append(''.join(c for c in word if (c not in punctuation) or (c == '-')))
        print(my_words)
        return my_words

    def suffix(self, word):
        """Creates a new word and removes one suffix at a time
        """
        for suffix in self.suffixes:
            # If the word ends with the particular suffix, create a new word by removing that suffix
            if word.endswith(suffix) and (word[:word.rfind(suffix)] in self.words):
                word = word[:word.rfind(suffix)]

        return word

    def converter(self, word):
        """Converts changed suffixes and roots to their original forms
        """
        q_list = ['lig', 'lug', 'lag', 'cig', 'cag', 'ig', 'lıg', 'cıg', 'ıg']
        k_list = ['liy', 'luy', 'cey', 'iy', 'uy', 'ey']
        t_list = ['ed', 'ged', 'yarad']

        # If the word ends with items of q_list, replace the last char with 'q'
        for suffix in q_list:
            if word.endswith(suffix):
                l = list(word)
                l[-1] = 'q'
                return "".join(l)
        # If the word ends with items of k_list, replace the last char with 'k'
        for suffix in k_list:
            if word.endswith(suffix):
                word = self.suffix(word)
                if word.endswith(suffix):
                    l = list(word)
                    l[-1] = 'k'
                    return "".join(l)
        # If the word is in t_list, replace the last char with 't'
        for item in t_list:
            if word == item:
                l = list(word)
                l[-1] = 't'
                return "".join(l)

        return word


    def stem_word(self, word):
        """Returns the stemmed version of word
        """
        # Convert if the word has changed root or suffix
        word = self.converter(word)
        # If word is already in the list, append it to stems list
        if word.isnumeric():
            self.stems.append(word)
        else:
            if word in self.words:
                self.stems.append(word)

        # Iterate through suffixes
        for suffix in self.suffixes:
            # If word ends with current suffix, remove the suffix and stem again
            if word.endswith(suffix):
                self.stem_word(word[:word.rfind(suffix)])

    def stem_words(self, list_of_words):
        """Returns stemmed versions of the words from txt file"""
        # Iterate over the range of word indexes
        list_of_stems = []
        for word in list_of_words:
            # Empty the stems list for each word
            self.stems = []
            # Apply stemming to each word in the list.
            self.stem_word(word)
            selected_stem = ""
            # Choose the stem with the maximum length
            for stem in self.stems:
                if len(stem) > len(selected_stem): selected_stem = stem
            # If there is no selected stem for word, append the word itself
            if selected_stem == "":
                selected_stem = word
            # Append the stem of the current word to the list of stems
            list_of_stems.append(selected_stem)
        # Return the updated list.
        print(list_of_stems)
        return list_of_stems
