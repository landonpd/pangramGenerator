import string
import ml_llama as llama

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

def pangram_stats_print(pangram,target_wrds=-1,target_chars=-1): #Make it so that when we don't have a target num or chars it still prints out the stats
    is_pan,missing_let=is_pangram(pangram)
    good_len_wrds,len_wrds=is_good_len(pangram,target_wrds,num_words)
    good_len_char,len_char=is_good_len(pangram,target_chars,num_char)
    results=f"here is the generated pangram: \"{pangram}\"\n"
    if is_pan:
        results+="It is a valid pangram, yayyyyyyy!!!"
    else:
        results+=f"It is not a valid pangram, missing letters: {missing_let}"
    if target_wrds>0:
        if good_len_wrds:
            wrd_count_str=f"\nThe number of words in the pangram was valid, it was {len_wrds} words long which was less than or equal to the target of {target_wrds}"
        else:
            wrd_count_str=f"\nThe number of words in the pangram was invalid, it was {len_wrds} words long which was less than or equal to the target of {target_wrds}"
    else:
        wrd_count_str=f"\nThere are {len_wrds} words in the pangram."
    results+=wrd_count_str
    if target_chars>0:
        if good_len_char:
            char_count_str=f"\nThe number of characters in the pangram was valid, it was {len_char} characters long which was less than or equal to the target of {target_chars}"
        else:
            char_count_str=f"\nThe number of characters in the pangram was invalid, it was {len_char} characters long which was less than or equal to the target of {target_chars}"
    else:
        char_count_str=f"\nThere are {len_char} characters in the pangram."
    results+=char_count_str
    return results #probably return instead of print

def pangram_stats(pangram): #returns if it was a pangram, the list of missing letters, the number of words and the number of characters
    is_pan,missing_let=is_pangram(pangram)
    len_wrds=num_words(pangram)
    len_char=num_char(pangram)
    return (is_pan,missing_let,len_wrds,len_char)

def char_to_int(char):
    return ord(char)-97

def test_missing_let_freq(pangrams):
    missing_char_counts=[0 for i in range(26)]
    results=()
    wrong_counts=0
    for pan in pangrams:
        results=pangram_stats(pan)
        if not results[0]:
            wrong_counts+=1
        for let in results[1]:
            missing_char_counts[char_to_int(let)]+=1
    return missing_char_counts,wrong_counts

def stats_aggregation(pangrams):
    is_pan=False
    len_wrd=0
    len_char=0
    is_pans=[]
    len_wrds=[]
    len_chars=[]
    distances=[]
    for pan in pangrams:
        distances.append(edit_distance_ave(pan,pangrams))
        is_pan,_,len_wrd,len_char=pangram_stats(pan)
        is_pans.append(is_pan)
        len_wrds.append(len_wrd)
        len_chars.append(len_char)
    return is_pans,len_wrds,len_chars,distances

def ave(arr):
    return round(sum(arr)/len(arr),3)

def edit_distance_ave(pan,pan_lst): #
    distances=[]
    pan_len=len(pan)
    for txt in pan_lst:
        if txt!=pan:
            distances.append(edit_distance(pan,txt,pan_len,len(txt)))

    return ave(distances)

def edit_distance(str1, str2, m, n, d = {}):

    key = m, n

    # If first string is empty, the only option
    # is to insert all characters of second
    # string into first
    if m == 0:
        return n

    # If second string is empty, the only
    # option is to remove all characters
    # of first string
    if n == 0:
        return m

    if key in d:
        return d[key]

    # If last characters of two strings are same,
    # nothing much to do. Ignore last characters
    # and get count for remaining strings.
    if str1[m - 1] == str2[n - 1]:
        return edit_distance(str1, str2, m - 1, n - 1)

    # If last characters are not same, consider
    # all three operations on last character of
    # first string, recursively compute minimum
    # cost for all three operations and take
    # minimum of three values.

    # Store the returned value at dp[m-1][n-1]
    # considering 1-based indexing
    d[key] = 1 + min(edit_distance(str1, str2, m, n - 1), # Insert
                     edit_distance(str1, str2, m - 1, n), # Remove
                     edit_distance(str1, str2, m - 1, n - 1)) # Replace
    return d[key]

# analyze the below to help fine tune default prompt
# missing letter frequencey Got function
# maybe letter frequencey
# variation in the responces, use algo function
# number of words Got function
# number of chars Got function
#
#
# pangram         : The quick brown fox jumps over the lazy dog.
# number of words : 9
# number of chars : 35
# missing letters : [] #['a','c']
#
#


# print(num_char("Pack my box with five dozen liquor jugs."))
# print(num_char("The quick brown fox jumps over the lazy dog"))
# print(num_char("The five boxing wizards jump quickly."))
arr=["test1asd;jklhfasd;jklfhasd;","hello World!","cheesecake","test2asdl;jkhfsdkl;bhjfjk;sdh"]
print(edit_distance(arr[0],arr[-1],len(arr[0]),len(arr[-1])))
print(edit_distance_ave(arr[0],arr))
