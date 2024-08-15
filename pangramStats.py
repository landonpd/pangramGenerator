#double check this whole thing

import string

class PangramStats:
    def __init__(self, pangram):
        self.pangram = pangram
        self.word_count = self.num_words()
        self.char_count = self.num_char()
        self.is_valid, self.missing_letters = self.is_pangram()

    def num_words(self):
        return len(self.pangram.split())

    def num_char(self):
        result_str = self.pangram.replace(' ', '')
        for char in string.punctuation:
            result_str = result_str.replace(char, '')
        return len(result_str)

    def is_pangram(self):
        found = False
        missing_let = []
        text = self.pangram.lower()
        for letter in string.ascii_lowercase:
            if letter in text:
                found = True
            else:
                missing_let.append(letter)
            found = False
        return len(missing_let) == 0, missing_let

    def is_good_len(self, target, counter):
        length = counter()
        return length <= target, length

    @staticmethod
    def edit_distance(str1, str2, m, n, d={}):
        key = m, n
        if m == 0:
            return n
        if n == 0:
            return m
        if key in d:
            return d[key]
        if str1[m - 1] == str2[n - 1]:
            return PangramStats.edit_distance(str1, str2, m - 1, n - 1)
        d[key] = 1 + min(PangramStats.edit_distance(str1, str2, m, n - 1),
                         PangramStats.edit_distance(str1, str2, m - 1, n),
                         PangramStats.edit_distance(str1, str2, m - 1, n - 1))
        return d[key]

    @staticmethod
    def ave(arr):
        return round(sum(arr) / len(arr), 3)

    def edit_distance_ave(self, pan_lst):
        distances = []
        pan_len = len(self.pangram)
        for txt in pan_lst:
            if txt != self.pangram:
                distances.append(self.edit_distance(self.pangram, txt, pan_len, len(txt)))
        return self.ave(distances)

    def stats_print(self, target_wrds=-1, target_chars=-1):
        results = f'Here is the generated pangram: "{self.pangram}"\n'
        if self.is_valid:
            results += "It is a valid pangram, yayyyyyyy!!!"
        else:
            results += f"It is not a valid pangram, missing letters: {self.missing_letters}"

        if target_wrds > 0:
            good_len_wrds, _ = self.is_good_len(target_wrds, self.num_words)
            if good_len_wrds:
                wrd_count_str = f"\nThe number of words in the pangram was valid, it was {self.word_count} words long which was less than or equal to the target of {target_wrds}"
            else:
                wrd_count_str = f"\nThe number of words in the pangram was invalid, it was {self.word_count} words long which was greater than the target of {target_wrds}"
        else:
            wrd_count_str = f"\nThere are {self.word_count} words in the pangram."
        results += wrd_count_str

        if target_chars > 0:
            good_len_char, _ = self.is_good_len(target_chars, self.num_char)
            if good_len_char:
                char_count_str = f"\nThe number of characters in the pangram was valid, it was {self.char_count} characters long which was less than or equal to the target of {target_chars}"
            else:
                char_count_str = f"\nThe number of characters in the pangram was invalid, it was {self.char_count} characters long which was greater than the target of {target_chars}"
        else:
            char_count_str = f"\nThere are {self.char_count} characters in the pangram."
        results += char_count_str

        return results
