#double check this whole thing

import string
import ml_llama as llama

class Pangram:
#going to just have pangram and is_valid, need new is_pangram function to override the one in this class
    def __init__(self, pan):
        self._pangram = pan
        self._is_valid = self.__is_pangram()
    def __is_pangram(self): #good, maybe make private
        text = self.pangram.lower()
        for letter in string.ascii_lowercase:
            if letter not in text:
                return False
        return True
    @property
    def pangram(self):
        return self._pangram

    @property
    def is_valid(self):
        return self._is_valid

class PangramStats(Pangram):
    def __init__(self, pan,model): #would need to take in a model to actually store tokens, maybe I make this one settable?
        super().__init__(pan) #ask claude how I can make a pangramstats with a Pangram
        self._wrd_cnt = self.__num_words()
        self._char_cnt = self.__num_char()
        self._tok_cnt = llama.count_tokens(self.pangram,model)
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
        missing_let = []
        text = self.pangram.lower()
        for letter in string.ascii_lowercase:
            if letter not in text:
                missing_let.append(letter)
        return  missing_let

    #getters that make the member variables read only essentially
    @property
    def pangram(self):
        return self._pangram

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
    def is_valid(self):
        return self._is_valid

    @property
    def missing_letters(self):
        return self._missing_lets



    def wrd_target(self, target): #maybe split into two functions probably,
        return self.wrd_cnt <= target

    def char_target(self, target): #maybe split into two functions probably,
        return self.char_cnt <= target


    def __str__(self):
            validity = "valid" if self._is_valid else "invalid"
            missing = f", missing letters: {self._missing_lets}" if not self._is_valid else ""
            return (f"Pangram: \"{self._pangram}\"\n"
                    f"Status: This is a {validity} pangram{missing}\n"
                    f"Word count: {self._wrd_cnt}\n"
                    f"Character count: {self._char_cnt}\n"
                    f"Token count: {self._tok_cnt}")


    # def stats_print(self, target_wrds=-1, target_chars=-1): #good, maybe change to be the print override and make the string more like the one in analyze
    #     results = f'Here is the generated pangram: "{self.pangram}"\n'
    #     if self.is_valid:
    #         results += "It is a valid pangram, yayyyyyyy!!!"
    #     else:
    #         results += f"It is not a valid pangram, missing letters: {self.missing_letters}"

    #     if target_wrds > 0:
    #         good_len_wrd = self.wrd_target(target_wrds)
    #         if good_len_wrd:
    #             wrd_count_str = f"\nThe number of words in the pangram was valid, it was {self.wrd_cnt} words long which was less than or equal to the target of {target_wrds}"
    #         else:
    #             wrd_count_str = f"\nThe number of words in the pangram was invalid, it was {self.wrd_cnt} words long which was greater than the target of {target_wrds}"
    #     else:
    #         wrd_count_str = f"\nThere are {self.wrd_cnt} words in the pangram."
    #     results += wrd_count_str

    #     if target_chars > 0:
    #         good_len_char = self.char_target(target_chars)
    #         if good_len_char:
    #             char_cnt_str = f"\nThe number of characters in the pangram was valid, it was {self.char_cnt} characters long which was less than or equal to the target of {target_chars}"
    #         else:
    #             char_cnt_str = f"\nThe number of characters in the pangram was invalid, it was {self.char_cnt} characters long which was greater than the target of {target_chars}"
    #     else:
    #         char_cnt_str = f"\nThere are {self.char_cnt} characters in the pangram."
    #     results += char_cnt_str

    #     return results
