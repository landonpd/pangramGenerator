'''
File with functions to test aspects of the pangrams being generated, using this file to fine tune my prompts
'''

import string
import ml_llama as llama
import pangram as ps

#maybe put these type of functions somewhere else entirely
def char_to_int(char):
    return ord(char)-97

def int_to_char(char):
    return char(char+97)

def ave(arr):
    return round(sum(arr)/len(arr),3)

def to_percent(num):
    return str(round(100*num,2))+"%"
#calculates how far apart two strings are and returns the value
def edit_distance(str1, str2, m, n, d = {}):
    key = m, n
    # If first string is empty, the only option is to insert all characters of second string into first

    if m == 0:
        return n
    # If second string is empty, the only option is to remove all character of first string

    if n == 0:
        return m

    if key in d:
        return d[key]
    # If last characters of two strings are same, nothing much to do. Ignore last characters and get count for remaining strings.

    if str1[m - 1] == str2[n - 1]:
        return edit_distance(str1, str2, m - 1, n - 1)

    # If last characters are not same, consider all three operations on last character of first string, recursively compute minimum
    # cost for all three operations and take minimum of three values. Store the returned value at dp[m-1][n-1] considering 1-based indexing
    d[key] = 1 + min(edit_distance(str1, str2, m, n - 1), # Insert
                     edit_distance(str1, str2, m - 1, n), # Remove
                     edit_distance(str1, str2, m - 1, n - 1)) # Replace
    return d[key]

#finds the average edit distance from a string to every string in a provided list
def edit_distance_ave(pangram,pan_lst): #takes in a pangramStats and a panstats_lst, really consider using string and string[] instead
    distances=[]
    pan_len=len(pangram.pangram)
    for pan in pan_lst:
        if pan!=pan:
            distances.append(edit_distance(pangram.pangram,pan.pangram,pan_len,len(pan.pangram)))

    return ave(distances)


#counts the number of times each letter was missing letters and returns the list
# def missing_let_freq(pangrams): #takes in a pangramStats
#     missing_char_counts=[0 for i in range(26)]
#     wrong_counts=0
#     for pan in pangrams:
#         for let in pan.missing_let:
#             missing_char_counts[char_to_int(let)]+=1
#     return missing_char_counts #,wrong_counts

#counts the number of correct pans, takes in PanStats
def num_correct(pangrams):
    cnt=0
    for pan in pangrams:
        if pan.is_pan:
            cnt+=1
    return cnt
#counts the number of incorrect pans, takes in panStats
def num_wrong(pangrams):
    cnt=0
    for pan in pangrams:
        if not pan.is_pan:
            cnt+=1
    return cnt

#takes the stats of the entire list of pangrams and returns all of them as seperate lists, maybe not needed anymore
def stats_aggregation(pangrams):
    pans=[]
    is_pans=[]
    wrd_cnts=[]
    char_cnts=[]
    tok_cnts=[]
    missing_char_cnt=[0 for i in range(26)]
    # distances=[]
    for pan in pangrams:
        # pans.append(pan.pangram)
        #is_pan,_,len_wrd,len_char=pangram_stats(pan)
        is_pans.append(pan.is_pan)
        wrd_cnts.append(pan.wrd_cnt)
        char_cnts.append(pan.char_cnt)
        tok_cnts.append(pan.tok_cnt)
        for let in pan.missing_let:
            missing_char_cnt[char_to_int(let)]+=1

    return is_pans,wrd_cnts,char_cnts,tok_cnts,missing_char_cnt#,distances





# analyze the below to help fine tune default prompt
# missing letter frequencey Got function
# maybe letter frequencey
# variation in the responces, use algo function
# number of words Got function
# number of chars Got function
#To make sence of avereage edit distnace, make random strings of the average length and then find the average distance between those,
#
# pangram         : A quick brown fox jumps over the lazy dog.
# number of words : 9
# number of chars : 33
# missing letters : [] #['a','c']
#
#


def main():
    #default values for user inputted parameters, can also be used for testing here
    st=""#"The universe is a lie"
    phrases=[]#["I like potatoes","hello World"]
    target_wrd=-1
    target_char=-1
    num_pans=100
    generator_tracker=(num_pans/20)//1
    model=llama.create_model(llama.MODEL_PATH)

    full_prompt,_=llama.create_prompt(st,phrases,target_wrd,target_char)

    pangrams=[]
    #generate num_pan pangrams, then calculate their tokens, maybe doing this somewhere else
    for i in range(num_pans):
        pangrams.append(ps.PangramStats(llama.create_pangram(model,full_prompt),model))
        if i%generator_tracker==0 and 1!=0: #quick thing to help track progress for longer tests
            print(f"\n\n{i} pangrams generated\n\n")

    #aggregating data from all pangrams
    is_pans,wrd_cnts,char_cnts,tok_cnts,missing_let=stats_aggregation(pangrams)

    #printing letter frequency stuff, including max and min
    max=min=missing_let[0]
    max_ind=min_ind=0
    for i in range(len(missing_let)):
        if missing_let[i]>max:
            max=missing_let[i]
            max_ind=0
        if missing_let[i]<min:
            min=missing_let[i]
            min_ind=i
        print(f"{string.ascii_lowercase[i]}:{missing_let[i]}")
    print(f"The most missed letter was {int_to_char(max_ind)} with {max} times missing")
    print(f"The least missed letter was {int_to_char(min_ind)} with only {min}")

    #printing out the pangrams
    print(f"\n\nHere are the {num_pans} generated pangrams.\n")
    for pan in pangrams: #maybe only print the true ones
        print(f"{pan}\n------\n")

    wrong=num_wrong(pangrams)
    correct=num_correct(pangrams)
    print(f"number of false pangrams: {wrong} out of {num_pans}, {to_percent(wrong/num_pans)}%.")
    print(f"number of false pangrams: {correct} out of {num_pans}, {to_percent(wrong/num_pans)}%.")
    print(f"average num of tokens: {ave(tok_cnts)}\naverage num of words: {ave(wrd_cnts)}\naverage num of characters: {ave(char_cnts)}")

#\naverage edit distance: {analyze.ave(distances)}, ok only missing distance stats now
if __name__=="__main__":
    main()
