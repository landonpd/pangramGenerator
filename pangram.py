#double check this whole thing

import string

class Pangram:
#going to just have pangram and is_valid, need new is_pangram function to override the one in this class
    def __init__(self, pan):
        self._pangram = pan
        self._is_pan = self.__is_pangram()
    def __is_pangram(self):
        text = self.pangram.lower()
        for letter in string.ascii_lowercase:
            if letter not in text:
                return False
        return True
    #essentially getters
    @property
    def pangram(self):
        return self._pangram

    @property
    def is_pan(self):
        return self._is_pan

    def __str__(self):
        validity="valid" if self.is_pan else "invald"
        return (f"Pangram: \"{self._pangram}\"\n"
                f"Validity: {validity}\n")

class PangramStats():
    def __init__(self, pan,model): #would need to take in a model to actually store tokens, maybe I make this one settable?
        self._pangram=pan.pangram
        self._is_pan=pan.is_pan
        self._wrd_cnt = self.__num_words()
        self._char_cnt = self.__num_char()
        self._tok_cnt = self.__count_tokens(self.pangram,model)
        self._missing_lets = self.__missing_let()
        #maybe include tok_cnt, it is a stat of the pangram

    #private internal functions used to calculate stuff
    def __num_words(self): #good, maybe make private
        return len(self._pangram.split())

    def __num_char(self): #good, maybe make private
        result_str = self._pangram.replace(' ', '')
        for char in string.punctuation:
            result_str = result_str.replace(char, '')
        return len(result_str)

    def __missing_let(self): #good, maybe make private
        if self._is_pan:
            return []
        missing_let = []
        text = self.pangram.lower()
        for letter in string.ascii_lowercase:
            if letter not in text:
                missing_let.append(letter)
        return  missing_let

    def __count_tokens(self,text,model): #one token is about 4 letters
        tokens=model.tokenize(text.encode())
        return len(tokens)
    #getters that make the member variables read only essentially
    @property
    def pangram(self):
        return self._pangram

    @property
    def is_pan(self):
        return self._is_pan

    @property
    def wrd_cnt(self):
        return self._wrd_cnt

    @property
    def char_cnt(self):
        return self._char_cnt

    @property
    def tok_cnt(self):
        return self._tok_cnt

    @property
    def missing_lets(self):
        return self._missing_lets



    def wrd_target(self, target): #maybe split into two functions probably,
        return self.wrd_cnt <= target

    def char_target(self, target): #maybe split into two functions probably,
        return self.char_cnt <= target


    def __str__(self):
            return (f"Pangram: \"{self._pangram}\"\n"
                    f"Word count: {self._wrd_cnt}\n"
                    f"Character count: {self._char_cnt}")

    def stats_str(self): #prints out all of the stats instead of just the user relevant ones
        validity = "valid" if self._is_pan else "invalid"
        missing = f", missing letters: {self._missing_lets}" if not self._is_pan else ""
        return (f"Pangram: \"{self._pangram}\"\n"
                f"Status: This is a {validity} pangram{missing}\n"
                f"Word count: {self._wrd_cnt}\n"
                f"Character count: {self._char_cnt}\n"
                f"Token count: {self._tok_cnt}")
