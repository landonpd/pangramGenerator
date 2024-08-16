'''
File with functions to test aspects of the pangrams being generated, using this file to fine tune my prompts

analyze the below to help fine tune default prompt
missing letter frequencey Got function
maybe letter frequencey
variation in the responces, use algo function
number of words Got function
number of chars Got function
To make sence of avereage edit distnace, make random strings of the average length and then find the average distance between those,

pangram         : A quick brown fox jumps over the lazy dog.
number of words : 9
number of chars : 33
missing letters : [] #['a','c']


'''

import string
import os
import sys
from contextlib import contextmanager
from timeit import default_timer as timer
import ml_llama as llama
import pangram as ps
from datetime import datetime


LOG_FILE="logs/analysisTest.log"
CLEAR_AND_RETURN='\033c\033[H'
#maybe put these type of functions somewhere else entirely
def char_to_int(char):
    return ord(char)-97

def int_to_char(num):
    return chr((num+97))

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
        for let in pan.missing_lets:
            missing_char_cnt[char_to_int(let)]+=1

    return is_pans,wrd_cnts,char_cnts,tok_cnts,missing_char_cnt#,distances

#generates n pangrams
def generate_pangrams(n,model,prompt):
    pangrams=[]
    # generator_tracker=(n*.1)//1
    for i in range(n):
        pangrams.append(ps.PangramStats(ps.Pangram(llama.create_pangram(model,prompt)),model))
        # if i%generator_tracker==0 and i!=0: #quick thing to help track progress for longer tests
        print(f"{CLEAR_AND_RETURN}{to_percent(i/n)} of pangrams generated")
    return pangrams

#prints the letter freqency and
def letter_stats(missing_let):
    max=min=missing_let[0]
    max_ind=[]
    min_ind=[]
    for i in range(len(missing_let)):
        if missing_let[i]>max:
            max=missing_let[i]
            max_ind=[i]
        elif missing_let[i]==max:
            max_ind.append(i)
        if missing_let[i]<min:
            min=missing_let[i]
            min_ind=[i]
        elif missing_let[i]==min:
            min_ind.append(i)
        print(f"{string.ascii_lowercase[i]}:{missing_let[i]}")
    min_missed_lets=[int_to_char(n) for n in min_ind]
    max_missed_lets=[int_to_char(n) for n in max_ind]
    print(f"The most missed letter(s) was(were) {max_missed_lets}\nwhich was(were) missed {max} times.")
    print(f"The least missed letter(s) was(were):\n{min_missed_lets}\nwhich was(were) missed {min} times.")

#displays the panagrams and thier stats
def print_pans(pans,only_true=False):
    print(f"\n\nHere are the {len(pans)} generated pangrams.\n")
    for pan in pans:
        if not only_true or (pan.is_pan):
            print(f"{pan}\n------\n")

#look at better ways to get these in here without including them, should they just be in llama file?



def time_func(func,*args,**kargs):
    start = timer()
    func(*args,**kargs)
    end = timer()
    return end - start
    #print(f"It took {end - start:.6f} seconds to generate one true pangram with the prompt{}.")

#use with stdout_to_file(): opens file path, and prints to it instead of to the console
@contextmanager
def stdout_to_file(file_path):
    original_stdout = sys.stdout
    try:
        with open(file_path, 'a') as f:
            sys.stdout = f
            print("New Log:",end=" ")
            yield
            print(f"timestamp: {datetime.now().strftime("%H:%M:%S %m-%d-%Y ")}\n------------------------------------------------------------------------------------------------------------\n")
    finally:
        sys.stdout = original_stdout

def main():
    #default values for user inputted parameters, can also be used for testing here
    st=""#"The universe is a lie"
    phrases=[]#["I like potatoes","hello World"]
    target_wrd=-1
    target_char=-1
    num_pans=1000

    full_prompt,readable_prompt=llama.create_prompt(st,phrases,target_wrd,target_char)
    model=llama.create_model(llama.MODEL_PATH)
    print("model created, generating pangrams.")

    pangrams=generate_pangrams(num_pans,model,full_prompt)
    print("All pangrams generated.")
    #aggregating data from all pangrams
    is_pans,wrd_cnts,char_cnts,tok_cnts,missing_let=stats_aggregation(pangrams)

    #printing letter frequency stuff, including max and min
    with stdout_to_file(LOG_FILE):
        print(f"Testing letter frequencies on {num_pans} pangrams with emphasis on not missing m. Here is the full prompt:\n{readable_prompt}\nResults:")
        letter_stats(missing_let) #maybe don't have it print, maybe do so that I can use a context manager to send the thing to the place
    #printing out the pangrams
    # print(f"\n\nHere are the {num_pans} generated pangrams.\n")
    # for pan in pangrams: #maybe only print the true ones
    #     print(f"{pan}\n------\n")

    wrong=num_wrong(pangrams)
    correct=num_correct(pangrams)
    print(f"number of valid pangrams: {correct} out of {num_pans}, {to_percent(correct/num_pans)}.")
    print(f"number of invalid pangrams: {wrong} out of {num_pans}, {to_percent(wrong/num_pans)}.")
    print(f"average num of tokens: {ave(tok_cnts)}\naverage num of words: {ave(wrd_cnts)}\naverage num of characters: {ave(char_cnts)}")

#\naverage edit distance: {analyze.ave(distances)}, ok only missing distance stats now
if __name__=="__main__":
    main()
