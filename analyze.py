import string

def num_words(text):
    return len(text.split(' '))

def num_char(text):
    result_str=text.replace(' ','')
    for char in string.punctuation:
        result_str=result_str.replace(char,'')
    return len(result_str)

def is_good_len(text,target,counter):
    len=counter(text)
    return len<=target,len

def is_pangram(text):
    found=False
    missingLet=[]
    text=text.lower()
    for letter in string.ascii_lowercase:
        for char in text:
            if letter==char:
                found=True
                # print(f"found the letter {letter}")
                break
        if not found:
            missingLet.append(letter)
        found=False
    if len(missingLet)==0:
        return True,missingLet
    else:
        return False,missingLet

def pangram_stats(pangram,target_wrds=-1,target_chars=-1):
    is_pan,missing_let=is_pangram(pangram)
    results=f"here is the generated pangram: \"{pangram}\"\n"
    if is_pan:
        results=results+"It is a valid pangram, yayyyyyyy!!!"
    else:
        results=results+f"It is not a valid pangram, missing letters: {missing_let}"
    if target_wrds>0:
        good_len_wrds,len_wrds=is_good_len(pangram,target_wrds,num_words)
        if good_len_wrds:
            wrd_count_str=f"\nThe number of words in the pangram was valid, it was {len_wrds} words long which was less than or equal to the target of {target_wrds}"
        else:
            wrd_count_str=f"\nThe number of words in the pangram was invalid, it was {len_wrds} words long which was less than or equal to the target of {target_wrds}"
        results=results+wrd_count_str
    if target_chars>0:
        good_len_char,len_char=is_good_len(pangram,target_chars,num_char)
        if good_len_char:
            char_count_str=f"\nThe number of characters in the pangram was valid, it was {len_char} characters long which was less than or equal to the target of {target_chars}"
        else:
            char_count_str=f"\nThe number of characters in the pangram was invalid, it was {len_char} characters long which was less than or equal to the target of {target_chars}"
        results=results+char_count_str
    print(results) #probably return instead of print

# print(num_char("Pack my box with five dozen liquor jugs."))
# print(num_char("Mr. Jock, TV quiz Ph.D., bags few lynx."))
# print(num_char("The five boxing wizards jump quickly."))
