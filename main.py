#this will (hopefully) be an AI that can generate panagrams, and if I get that, then I will
#make it so that a user can enter either words or phrases that they want to be in the panagram
#Going to start with a function that can double check that the inputted sentence is a panagram

# ok, to finish this up,
# add user input, user chooses context for their sentence, so they could pick whimsical fantasy author, new york times editor etc., ask ai to give me more ideas probably
# Consider adding pretty ui, if it is easier than bubble tea than definitly, if not then leave it gross for now
# Consider making it so that when generating a function the results have to match params, so it has to start with the sentence starter, it has to have all the phrases, it has to be under the char and word limit. Could break because could cause infinite loop, would have to put a limiter on it.
#
#
# In analyze.py
# look at each individual optional parameter and make sure it works, (e.g num characters makes it longer right now)
# add a function that generates random strings, when testing edit distance make two strings of the average length and find thier edit distance from each other (or maybe do this like 50 times) to compare to the edit distance for the sentences, actual sentences have spaces and punctuation, so they are actually longer, don't know what to do with that
# Add function to time a function so I can see how it works

import string
import ml_llama as llama
import pangram as ps
#so 4 letters per token, average number of letters per word is 6.47 so lets say 7, if I want 20 words, thats 7*20/4 for number of tokens approximateyly, could use this to narrow down the max_token

#generates pangrams using the prompt until the result is a valid pangram
def generate_pangram(model,prompt):
    pan=ps.Pangram(llama.create_pangram(model,prompt))
    while not pan.is_pan:
        pan=ps.Pangram(llama.create_pangram(model,prompt))
    return ps.PangramStats(pan,model)

#generates variable amount of valid pangrams
def generate_true_pangram(model,prompt,num):
    pans=[]
    for i in range(num):
        pans.append(generate_pangram(model,prompt))
    return pans

def main():
    st=""#"The universe is a lie"
    phrases=[]#["I like potatoes","hello World"]
    target_wrd=-1
    target_char=-1
    num_pans=1
    #get user inputs for the above things
    st=input("Enter a sentence starter, click enter to forego a starter: ")
    # print(st)
    phrase=input("Enter phrases to include in your pangram, hit enter to stop entering phrases: ")

    while phrase!="":
        phrases.append(phrase)
        phrase=input("Enter phrases to include in your pangram, hit enter to stop entering phrases: ")

    # print(phrases)
    target_wrd=int(input("Enter a target number of words, enter -1 to forgoe a target: "))
    # print(target_wrd)
    target_wrd=int(input("Enter a target number of characters, enter -1 to forgoe a target: "))
    num_pans=int(input("enter how many pangrams you want generated: "))
    #create the model, generate the prompt,
    model=llama.create_model(llama.MODEL_PATH)
    full_prompt,_=llama.create_prompt(st,phrases,target_wrd,target_char)
    pangrams=generate_true_pangram(model,full_prompt,num_pans)
    for pan in pangrams:
        print(f"{pan}\n------\n") #pangram.stats_print(target_wrd,target_char)
    # if target_wrd!=-1:
    #     if pangram.char_target(target_wrd):
    #         print(f"The pangram has a valid number of characters,it has less than or {target_wrd} words.")
    #     else:
    #         print(f"The pangram has an invalid number of characters,it has more than {target_wrd} words.")
    # if target_char!=-1:
    #     if pangram.char_target(target_char):
    #         print(f"The pangram has a valid number of characters,it has less than or {target_char} characters.")
    #     else:
    #         print(f"The pangram has an invalid number of characters,it has more than {target_char} characters.")

if __name__=="__main__":
    main()
